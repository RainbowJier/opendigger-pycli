from __future__ import annotations
import copy
import datetime
import typing as t
from dataclasses import dataclass, field, replace

from rich.progress import track

from opendigger_pycli.datatypes import (
    NON_TRIVAL_NETWORK_INDICATOR_DATA,
    NON_TRIVIAL_INDICATOR_DATA,
    TRIVIAL_INDICATOR_DATA,
    TRIVIAL_NETWORK_INDICATOR_DATA,
    IndicatorQuery,
)
from opendigger_pycli.console import CONSOLE
from opendigger_pycli.utils.github_api import (
    create_issue,
    search_issue_title,
    create_issue_comment,
    get_issue_comments,
    create_issue_comment_reactions,
)
from opendigger_pycli.config.utils import get_github_pat, has_github_pat, get_user_info
from opendigger_pycli.utils import THREAD_POOL

if t.TYPE_CHECKING:
    from opendigger_pycli.datatypes import (
        BaseData,
        DataloaderProto,
        DataloaderResult,
        NonTrivalNetworkInciatorData,
        NonTrivialIndicatorData,
        TrivialIndicatorData,
        TrivialNetworkIndicatorData,
    )
    from opendigger_pycli.utils.github_api import IssueCommentInfoType, IssueInfoType


@t.overload
def run_dataloader(result: "RepoQueryResult") -> None:
    ...


@t.overload
def run_dataloader(result: "UserQueryResult") -> None:
    ...


def run_dataloader(result) -> None:
    if not isinstance(result, RepoQueryResult) and not isinstance(
        result, UserQueryResult
    ):
        raise TypeError("result must be RepoQueryResult or UserQueryResult")

    process_desc = (
        f"Fetching data for {result.type}: [green]{result.username}"
        if isinstance(result, UserQueryResult)
        else f"Fetching data for {result.type}: [green]{result.org_name}/{result.repo_name}"
    )
    for dataloader in track(result.dataloaders, description=process_desc):
        if not dataloader.pass_date:
            result.data[dataloader.name] = (
                dataloader.load(
                    result.org_name,
                    result.repo_name,
                )
                if isinstance(result, RepoQueryResult)
                else dataloader.load(result.username)
            )
            continue
        current_indicator_queries = [
            indicator_query[1]
            for indicator_query in result.indicator_queries
            if indicator_query[0] == dataloader.name and indicator_query[1] is not None
        ]
        # For indicators that do not specify a query and need to pass in a date query, ignore it directly
        if not current_indicator_queries:
            continue

        current_year = datetime.date.today().year
        dates = set()
        for query in current_indicator_queries:
            for month in query.months:
                dates.add((current_year, month))
            for year in query.years:
                for month in range(1, 13):
                    dates.add((year, month))
            for year_month in query.year_months:
                dates.add(year_month)

        result.data[dataloader.name] = (
            dataloader.load(result.org_name, result.repo_name, list(dates))
            if isinstance(result, RepoQueryResult)
            else dataloader.load(result.username, list(dates))
        )


def merge_indicator_queries(
    indicator_queries: t.List["IndicatorQuery"],
) -> "IndicatorQuery":
    need_years_list = [{year for year in query.years} for query in indicator_queries]
    need_years = set.union(*need_years_list) if need_years_list else set()
    need_months_list = [
        {month for month in query.months} for query in indicator_queries
    ]
    need_months = set.union(*need_months_list) if need_months_list else set()
    need_year_months_list = [
        {year_month for year_month in query.year_months} for query in indicator_queries
    ]
    need_year_months = (
        set.union(*need_year_months_list) if need_year_months_list else set()
    )
    return IndicatorQuery(
        years=frozenset(need_years),
        months=frozenset(need_months),
        year_months=frozenset(need_year_months),
    )


def query_base_data(
    base_data_list: t.List["BaseData"],
    indicator_queries: t.List["IndicatorQuery"],
):
    merged_indicator_query = merge_indicator_queries(indicator_queries)
    success_year_query = set()
    success_month_query = set()
    success_year_month_query = set()

    queried_data = []
    for base_data in base_data_list:
        is_add = False
        if base_data.value is None:
            continue
        if base_data.year in merged_indicator_query.years:
            success_year_query.add(base_data.year)
            is_add = True
        if base_data.month in merged_indicator_query.months:
            success_month_query.add(base_data.month)
            is_add = True
        if (
            base_data.year,
            base_data.month,
        ) in merged_indicator_query.year_months:
            success_year_month_query.add((base_data.year, base_data.month))
            is_add = True
        if not indicator_queries:
            is_add = True

        if not is_add:
            continue
        queried_data.append(base_data)

    faild_query = None
    if (
        merged_indicator_query.years - success_year_query
        or merged_indicator_query.months - success_month_query
        or merged_indicator_query.year_months - success_year_month_query
    ):
        faild_query = IndicatorQuery(
            years=merged_indicator_query.years - success_year_query,
            months=merged_indicator_query.months - success_month_query,
            year_months=merged_indicator_query.year_months,
        )

    return queried_data, faild_query


def query_non_trivial_indicator(
    indicator_data: "NonTrivialIndicatorData",
    indicator_queries: t.List["IndicatorQuery"],
) -> t.Tuple["NonTrivialIndicatorData", t.Dict[str, t.Optional["IndicatorQuery"]]]:
    queried_indicator_data = copy.deepcopy(indicator_data)
    failed_queries = {}
    for key, base_data_list in indicator_data.value.items():
        base_data_list = t.cast(t.List["BaseData"], base_data_list)
        queried_base_data, failed_query = query_base_data(
            base_data_list, indicator_queries
        )
        queried_indicator_data.value[key] = queried_base_data  # type: ignore
        failed_queries[key] = failed_query
    return queried_indicator_data, failed_queries


def query_trival_indicator(
    indicator_data: "TrivialIndicatorData",
    indicator_queries: t.List["IndicatorQuery"],
) -> t.Tuple["TrivialIndicatorData", t.Optional["IndicatorQuery"]]:
    queried_base_data_list, failed_query = query_base_data(
        indicator_data.value, indicator_queries
    )
    return replace(indicator_data, value=queried_base_data_list), failed_query


def query_non_trivial_network_indciator(
    indicator_data: "NonTrivalNetworkInciatorData",
    indicator_queries: t.List["IndicatorQuery"],
) -> t.Tuple["NonTrivalNetworkInciatorData", t.Optional["IndicatorQuery"]]:
    queried_base_data_list, failed_query = query_base_data(
        indicator_data.value, indicator_queries
    )
    return replace(indicator_data, value=queried_base_data_list), failed_query


def query_trivial_network_indicator(
    indicator_data: "TrivialNetworkIndicatorData",
    indicator_queries: t.List["IndicatorQuery"],
) -> t.Tuple["TrivialNetworkIndicatorData", t.Optional["IndicatorQuery"]]:
    return replace(indicator_data), None


class NodataIssueCreator:
    """
    用于创建关于NoData问题的GitHub问题的类。

    属性:
    title (str): 问题的标题。
    nodata_indicator_names (List[str]): 表示NoData的指标名称列表。
    _github_pat (str): GitHub的个人访问令牌，用于API访问。

    方法:
    __init__: 类的构造函数，初始化问题标题、NoData指标名称，并设置GitHub个人访问令牌。
    """

    _github_pat: str

    def __init__(self, title: str, nodata_indicator_names: t.List[str]) -> None:
        """
        初始化NodataIssueCreator实例。

        参数:
        title (str): 将要创建的GitHub问题的标题。
        nodata_indicator_names (List[str]): 与问题相关的NoData指标名称列表。
        """
        self.title = title
        self.nodata_indicator_names = nodata_indicator_names

        # 获取GitHub个人访问令牌
        self._github_pat = get_github_pat()

        # 搜索已存在的GitHub问题
        self.has_issue, self.issue_infos = search_issue_title(
            "RainbowJier",
            "opendigger-pycli",
            self.title,
            ["nodata", "bot"],
            self._github_pat,
        )

        # 初始化存储已存在问题信息的字典
        self.existed_issue_map: t.Dict[int, IssueInfoType] = {}
        self.existed_nodata_infos: t.Dict[int, t.List[IssueCommentInfoType]] = {}

        # 如果已存在相同标题的问题，则填充已存在问题的映射
        if self._has_existed_issue:
            for issue_info in self.issue_infos:
                self.existed_issue_map[issue_info["issue_number"]] = issue_info


    @property
    def _has_existed_issue(self) -> bool:
        """
        检查实例是否已有问题
        该属性检查实例是否有问题以及是否有具体的问题信息。
        它不接受任何参数，并返回一个布尔值，指示实例是否已经存在问题。
        @return bool 返回True如果实例已有问题且有关该问题的具体信息存在，否则返回False。
        """
        # 检查是否有问题以及是否有具体的问题信息
        return bool(self.has_issue and self.issue_infos)

    def _create_nodata_issue(self) -> bool:
        """
        创建一个关于缺失数据的问题（issue）。
        如果已存在相关问题，则尝试获取每个问题的评论信息，并更新存在缺失数据信息的记录。
        如果问题不存在，则尝试创建一个新的问题，并记录创建成功的问题信息。
        返回值:
            bool: 如果成功创建问题或获取已存在问题的信息，则返回True；否则返回False。
        """
        if self._has_existed_issue:
            # 遍历所有问题信息，尝试获取并更新已存在缺失数据问题的评论信息
            for issue_info in self.issue_infos:
                (
                    _,
                    self.existed_nodata_infos[issue_info["issue_number"]],
                ) = get_issue_comments(
                    issue_api_url=issue_info["issue_api_url"],
                    github_pat=self._github_pat,
                )
            return True

        # 尝试创建一个新的缺失数据问题
        is_success, issue_info = create_issue(
            "RainbowJier",
            "opendigger-pycli",
            self._github_pat,
            self.title,
            labels=["nodata", "bot"],
            assignees=["RainbowJier"],
        )
        if is_success and issue_info:
            # 如果创建成功，记录问题信息，并初始化缺失数据的评论信息为空列表
            self.existed_issue_map[issue_info["issue_number"]] = issue_info
            self.existed_nodata_infos[issue_info["issue_number"]] = []
            return True
        return False


    class YourClassName:
        def _add_nodata_info(self) -> None:
            """
            为没有数据的指标添加信息。
            遍历nodata_indicator_names列表中的每个指标名称，检查是否已经在存在的issue评论中提到了这个指标。
            如果提到，则为该评论添加"eyes"反应；如果未提到，则在第一个存在的issue中添加一条评论，指出缺少该指标的数据。
            """
            for indicator_name in self.nodata_indicator_names:
                is_ok = False  # 标记是否已经处理过当前指标

                # 检查每个已存在的issue评论中是否提到了当前指标
                for _, issue_comment_infos in self.existed_nodata_infos.items():
                    for issue_comment_info in issue_comment_infos:
                        # 如果评论中包含当前指标，则为该评论添加"eyes"反应
                        if indicator_name not in issue_comment_info["body"]:
                            continue
                        create_issue_comment_reactions(
                            issue_cooment_api_url=issue_comment_info[
                                "issue_comment_api_url"
                            ],
                            content="eyes",
                            github_pat=self._github_pat,
                        )
                        is_ok = True  # 标记已处理
                        break
                    if is_ok:
                        break  # 如果当前指标已处理，跳出内层循环

                if is_ok:
                    continue  # 如果当前指标已处理，继续下一个指标

                # 如果当前指标未在任何评论中被提到，则在第一个存在的issue中添加评论
                create_issue_comment(
                    issue_api_url=list(self.existed_issue_map.values())[0]["issue_api_url"],
                    body=f"No Indicator Data: {indicator_name}",
                    github_pat=self._github_pat,
                )

        def run(self) -> None:
            """
            执行数据检查并处理无数据指标的流程。
            尝试创建无数据的issue，如果成功，则添加无数据信息；如果过程中出现异常，则静默处理异常。
            """
            try:
                # 如果无法创建无数据的issue，则直接返回
                if not self._create_nodata_issue():
                    return
                self._add_nodata_info()  # 添加无数据信息
            except Exception:
                return  # 静默处理异常


def run_query(query_result: "BaseQueryResult") -> None:
    indicator_queries = query_result.indicator_queries
    indicators_data = query_result.data

    nodata_indicator_names = []
    for (
        indicator_name,
        indicator_dataloder_result,
    ) in indicators_data.items():
        query_result.failed_query[indicator_name] = None
        current_indicator_queries = (
            [
                indicator_query[1]
                for indicator_query in indicator_queries
                if indicator_query[0] == indicator_name
                and indicator_query[1] is not None
            ]
            if query_result.uniform_query is None
            else [query_result.uniform_query]
        )
        if (
            not indicator_dataloder_result.is_success
            or not indicator_dataloder_result.data
        ):
            nodata_indicator_names.append(indicator_name)
            continue

        indicator_data_class = indicator_dataloder_result.data.data_class
        queried_indciator_data: t.Any
        if indicator_data_class == TRIVIAL_NETWORK_INDICATOR_DATA:
            (
                queried_indciator_data,
                failed_query,
            ) = query_trivial_network_indicator(
                indicator_dataloder_result.data, current_indicator_queries
            )
        elif indicator_data_class == NON_TRIVAL_NETWORK_INDICATOR_DATA:
            (
                queried_indciator_data,
                failed_query,
            ) = query_non_trivial_network_indciator(
                indicator_dataloder_result.data, current_indicator_queries
            )
        elif indicator_data_class == TRIVIAL_INDICATOR_DATA:
            (
                queried_indciator_data,
                failed_query,
            ) = query_trival_indicator(
                indicator_dataloder_result.data, current_indicator_queries
            )
        elif indicator_data_class == NON_TRIVIAL_INDICATOR_DATA:
            (
                queried_indciator_data,
                failed_queries,
            ) = query_non_trivial_indicator(
                indicator_dataloder_result.data, current_indicator_queries
            )
            failed_query_dict = {}
            for key, failed_query in failed_queries.items():
                failed_query_dict[key] = failed_query
            query_result.failed_query[indicator_name] = failed_query_dict
            query_result.queried_data[indicator_name] = replace(
                indicator_dataloder_result, data=queried_indciator_data
            )
            continue
        else:
            raise ValueError(
                f"Unknown indicator data class: {indicator_dataloder_result}"
            )
        query_result.failed_query[indicator_name] = failed_query
        query_result.queried_data[indicator_name] = replace(
            indicator_dataloder_result, data=queried_indciator_data
        )

    if not nodata_indicator_names:
        return

    if query_result.type == "user":
        query_result = t.cast("UserQueryResult", query_result)
        title = f"User: {query_result.username}"
        print_str = f"{title}, Indicator Names: {str(nodata_indicator_names)}, No Data"
    else:
        query_result = t.cast("RepoQueryResult", query_result)
        title = f"Repo: {query_result.org_name}/{query_result.repo_name}"
        print_str = f"{title}, Indicator Names: {str(nodata_indicator_names)}, No Data"

    CONSOLE.print(f"[red]{print_str}[/red]")
    if not has_github_pat():
        CONSOLE.print(
            "[yellow]You can config github personal access token to create issues automatically[/yellow]"
        )
        return
    with CONSOLE.status("Issues being returned to OpenDigger..."):
        NodataIssueCreator(title, nodata_indicator_names).run()


@dataclass
class BaseQueryResult:
    type: t.ClassVar[t.Literal["user", "repo"]]
    dataloaders: t.List["DataloaderProto"]
    indicator_queries: t.List[t.Tuple[str, t.Optional["IndicatorQuery"]]]
    uniform_query: t.Optional["IndicatorQuery"]
    data: t.Dict[str, "DataloaderResult"] = field(default_factory=dict, init=False)
    queried_data: t.Dict[str, "DataloaderResult"] = field(
        default_factory=dict, init=False
    )
    failed_query: t.Dict[
        str,
        t.Union[
            t.Optional["IndicatorQuery"],
            t.Dict[str, t.Optional["IndicatorQuery"]],
        ],
    ] = field(default_factory=dict, init=False)


@dataclass
class RepoQueryResult(BaseQueryResult):
    type: t.ClassVar[t.Literal["repo"]] = "repo"
    repo: t.Tuple[str, str]
    org_name: str = field(init=False)
    repo_name: str = field(init=False)

    def __post_init__(self) -> None:
        self.org_name, self.repo_name = self.repo
        run_dataloader(self)
        run_query(self)


@dataclass
class UserQueryResult(BaseQueryResult):
    type: t.ClassVar[t.Literal["user"]] = "user"
    username: str

    def __post_init__(self) -> None:
        run_dataloader(self)
        run_query(self)


QueryResults = t.Union[t.List["RepoQueryResult"], t.List["UserQueryResult"]]
