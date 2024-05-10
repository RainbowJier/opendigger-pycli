import typing as t

from opendigger_pycli.datatypes import (
    AcceptedChangeRequestData,
    ActiveDateAndTimeData,
    AddedCodeChangeLineData,
    BusFactorData,
    ChangeRequestAgeData,
    ChangeRequestData,
    ChangeRequestResolutionDurationData,
    ChangeRequestResponseTimeData,
    ChangeRequestReviewData,
    ClosedIssueData,
    DataloaderResult,
    InactiveContributorData,
    IssueAgeData,
    IssueCommentData,
    IssueResolutionDurationData,
    IssueResponseTimeData,
    NewContributorData,
    NewIssueData,
    ParticipantData,
    RemovedCodeChangeLineData,
    StarData,
    SumCodeChangeLineData,
    TechnicalForkData,
    ActivityDetailData,
)

from .base import BaseRepoDataloader, register_dataloader
from .utils import (
    get_repo_data,
    load_base_data,
    load_name_and_value,
    load_non_trival_indicator_data,
)

if t.TYPE_CHECKING:
    from opendigger_pycli.datatypes.dataloader import DataloaderProto


@register_dataloader
class ActiveDateAndTimeRepoDataloader(BaseRepoDataloader):
    name = "active_date_and_time"
    indicator_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/active_dates_and_times.json"

    def load(self, org: str, repo: str) -> DataloaderResult[ActiveDateAndTimeData]:
        data = get_repo_data(org, repo, ActiveDateAndTimeData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )
        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=ActiveDateAndTimeData(
                value=load_base_data(data, lambda x: [int(i) for i in x]),
            ),
            desc="",
        )


@register_dataloader
class StarRepoDataloader(BaseRepoDataloader):
    name = "star"
    indicator_type = "metric"
    introducer = "X-lab"
    demo_url = (
        "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/stars.json"
    )

    def load(self, org: str, repo: str) -> DataloaderResult[StarData]:
        data = get_repo_data(org, repo, StarData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )
        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=StarData(value=load_base_data(data, int)),
            desc="",
        )


@register_dataloader
class TechnicalForkRepoDataloader(BaseRepoDataloader):
    name = "technical_fork"
    indicator_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/technical_fork.json"

    def load(self, org: str, repo: str) -> DataloaderResult[TechnicalForkData]:
        data = get_repo_data(org, repo, TechnicalForkData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )
        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=TechnicalForkData(value=load_base_data(data, int)),
            desc="",
        )


@register_dataloader
class ParticipantRepoDataloader(BaseRepoDataloader):
    name = "participant"
    indicator_type = "metric"
    introducer = "X-lab"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/participants.json"

    def load(self, org: str, repo: str) -> DataloaderResult[ParticipantData]:
        data = get_repo_data(org, repo, ParticipantData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )
        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=ParticipantData(value=load_base_data(data, int)),
            desc="",
        )


@register_dataloader
class NewContributorRepoDataloader(BaseRepoDataloader):
    name = "new_contributor"
    indicator_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/new_contributors_detail.json"

    def load(self, org: str, repo: str) -> DataloaderResult[NewContributorData]:
        data = get_repo_data(org, repo, NewContributorData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=NewContributorData(
                value=load_base_data(data, lambda x: [str(i) for i in x]),
            ),
            desc="",
        )


@register_dataloader
class InactiveContributorRepoDataloader(BaseRepoDataloader):
    name = "inactive_contributor"
    indicator_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/inactive_contributors.json"

    def load(self, org: str, repo: str) -> DataloaderResult[InactiveContributorData]:
        data = get_repo_data(org, repo, InactiveContributorData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=InactiveContributorData(value=load_base_data(data, int)),
            desc="",
        )


@register_dataloader
class BusFactorRepoDataloader(BaseRepoDataloader):
    name = "bus_factor"
    indicator_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/bus_factor_detail.json"

    def load(self, org: str, repo: str) -> DataloaderResult[BusFactorData]:
        data = get_repo_data(org, repo, BusFactorData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=BusFactorData(
                value=load_base_data(
                    data, lambda x: [load_name_and_value(i) for i in x]
                ),
            ),
            desc="",
        )


# 注册为数据加载器的类，用于加载新问题指标的数据
@register_dataloader
class NewIssueRepoDataloader(BaseRepoDataloader):
    # 类级别的变量定义了数据加载器的名称、指标类型、引入者和演示URL
    name = "new_issue"
    indicator_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/issues_new.json"

    # 加载指定组织和仓库的新问题数据
    def load(self, org: str, repo: str) -> DataloaderResult[NewIssueData]:
        """
        加载指定仓库的新问题数据。

        参数:
        org (str): 组织名称。
        repo (str): 仓库名称。

        返回值:
        DataloaderResult[NewIssueData]: 数据加载结果，成功时包含新问题数据，失败时提供错误描述。
        """
        # 尝试获取仓库的新问题数据
        data = get_repo_data(org, repo, NewIssueData.name)
        if data is None:
            # 如果无法获取数据，返回失败结果
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )

        # 成功获取数据，返回数据加载结果
        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=NewIssueData(value=load_base_data(data, int)),
            desc="",
        )




# 注册为数据加载器的类，用于加载关闭的issue数据
@register_dataloader
class ClosedIssueRepoDataloader(BaseRepoDataloader):
    # 类级别的变量定义了数据加载器的名称、指标类型、引入者和演示URL
    name = "closed_issue"
    indicator_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/issues_closed.json"

    # 加载特定组织和仓库的关闭issue数据
    def load(self, org: str, repo: str) -> DataloaderResult[ClosedIssueData]:
        """
        加载指定组织和仓库的关闭issue数据

        参数:
        org (str): 组织名称
        repo (str): 仓库名称

        返回值:
        DataloaderResult[ClosedIssueData]: 数据加载结果，成功时包含关闭issue数据，失败时提供错误描述
        """
        # 尝试获取仓库的关闭issue数据
        data = get_repo_data(org, repo, ClosedIssueData.name)
        if data is None:
            # 如果无法获取数据，返回失败结果
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )

        # 如果成功获取数据，加载并返回数据结果
        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=ClosedIssueData(value=load_base_data(data, int)),
            desc="",
        )




# 注册为数据加载器的类，用于加载仓库的issue评论数据
@register_dataloader
class IssueCommentRepoDataloader(BaseRepoDataloader):
    # 类级别的变量定义了数据加载器的名称、指标类型、引入者和演示URL
    name = "issue_comment"
    indicator_type = "metric"
    introducer = "X-lab"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/issue_comments.json"

    # 加载指定仓库的issue评论数据
    def load(self, org: str, repo: str) -> DataloaderResult[IssueCommentData]:
        """
        加载指定组织和仓库的issue评论数据

        参数:
        org (str): 组织名称
        repo (str): 仓库名称

        返回值:
        DataloaderResult[IssueCommentData]: 数据加载结果，成功时包含issue评论数据，失败时提供错误描述
        """
        # 尝试获取仓库的issue评论数据
        data = get_repo_data(org, repo, IssueCommentData.name)
        if data is None:
            # 如果无法获取数据，返回失败结果
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )

        # 成功获取数据，返回数据加载结果
        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=IssueCommentData(value=load_base_data(data, int)),
            desc="",
        )



@register_dataloader
class IssueResponseTimeRepoDataloader(BaseRepoDataloader):
    name = "issue_response_time"
    indicator_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/issue_response_time.json"

    def load(self, org: str, repo: str) -> DataloaderResult[IssueResponseTimeData]:
        data = get_repo_data(org, repo, IssueResponseTimeData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=IssueResponseTimeData(value=load_non_trival_indicator_data(data)),
            desc="",
        )


@register_dataloader
class IssueResolutionDurationRepoDataloader(BaseRepoDataloader):
    name = "issue_resolution_duration"
    indicator_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/issue_resolution_duration.json"

    def load(
        self, org: str, repo: str
    ) -> DataloaderResult[IssueResolutionDurationData]:
        data = get_repo_data(org, repo, IssueResolutionDurationData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=IssueResolutionDurationData(
                value=load_non_trival_indicator_data(data)
            ),
            desc="",
        )


@register_dataloader
class IssueAgeRepoDataloader(BaseRepoDataloader):
    name = "issue_age"
    indicator_type = "metric"
    introducer = "CHAOSS"
    demo_url = (
        "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/issue_age.json"
    )

    def load(self, org: str, repo: str) -> DataloaderResult[IssueAgeData]:
        data = get_repo_data(org, repo, IssueAgeData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=IssueAgeData(
                value=load_non_trival_indicator_data(data),
            ),
            desc="",
        )


@register_dataloader
class AddedCodeChangeLineRepoDataloader(BaseRepoDataloader):
    name = "added_code_change_line"
    indicator_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/code_change_lines_add.json"

    def load(self, org: str, repo: str) -> DataloaderResult[AddedCodeChangeLineData]:
        data = get_repo_data(org, repo, AddedCodeChangeLineData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=AddedCodeChangeLineData(
                value=load_base_data(data, int),
            ),
            desc="",
        )


@register_dataloader
class RemovedCodeChangeLineRepoDataloader(BaseRepoDataloader):
    name = "removed_code_change_line"
    indicator_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/code_change_lines_remove.json"

    def load(self, org: str, repo: str) -> DataloaderResult[RemovedCodeChangeLineData]:
        data = get_repo_data(org, repo, RemovedCodeChangeLineData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=RemovedCodeChangeLineData(
                value=load_base_data(data, int),
            ),
            desc="",
        )


@register_dataloader
class SummedCodeChangeLineRepoDataloader(BaseRepoDataloader):
    name = "summed_code_change_line"
    indicator_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/code_change_lines_sum.json"

    def load(self, org: str, repo: str) -> DataloaderResult[SumCodeChangeLineData]:
        data = get_repo_data(org, repo, SumCodeChangeLineData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=SumCodeChangeLineData(
                value=load_base_data(data, int),
            ),
            desc="",
        )


@register_dataloader
class ChangeRequestRepoDataloader(BaseRepoDataloader):
    name = "change_request"
    indicator_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/change_requests.json"

    def load(self, org: str, repo: str) -> DataloaderResult[ChangeRequestData]:
        data = get_repo_data(org, repo, ChangeRequestData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=ChangeRequestData(
                value=load_base_data(data, int),
            ),
            desc="",
        )


@register_dataloader
class AcceptedChangeRequestRepoDataloader(BaseRepoDataloader):
    name = "accepted_change_request"
    indicator_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/change_requests_accepted.json"

    def load(self, org: str, repo: str) -> DataloaderResult[AcceptedChangeRequestData]:
        data = get_repo_data(org, repo, AcceptedChangeRequestData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=AcceptedChangeRequestData(
                value=load_base_data(data, int),
            ),
            desc="",
        )


@register_dataloader
class ChangeRequestReviewRepoDataloader(BaseRepoDataloader):
    name = "change_request_review"
    indicator_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/change_requests_reviews.json"

    def load(self, org: str, repo: str) -> DataloaderResult[ChangeRequestReviewData]:
        data = get_repo_data(org, repo, ChangeRequestReviewData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=ChangeRequestReviewData(
                value=load_base_data(data, int),
            ),
            desc="",
        )


@register_dataloader
class ChangeRequestResponseTimeRepoDataloader(BaseRepoDataloader):
    name = "change_request_response_time"
    indicator_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/change_request_response_time.json"

    def load(
        self, org: str, repo: str
    ) -> DataloaderResult[ChangeRequestResponseTimeData]:
        data = get_repo_data(org, repo, ChangeRequestResponseTimeData.name)
        if data is None:
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )

        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=ChangeRequestResponseTimeData(
                value=load_non_trival_indicator_data(data),
            ),
            desc="",
        )


# 为ChangeRequestResolutionDurationRepoDataloader类提供数据加载功能，
# 该类继承自BaseRepoDataloader，用于加载变更请求解决时长的数据。
@register_dataloader
class ChangeRequestResolutionDurationRepoDataloader(BaseRepoDataloader):
    # 类的属性定义
    name = "change_request_resolution_duration"  # 数据加载器的名称
    indicator_type = "metric"  # 指标的类型为度量指标
    introducer = "CHAOSS"  # 指标的引入者为CHAOSS社区
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/change_request_resolution_duration.json"  # 指标数据的演示URL

    # 加载特定组织和仓库的变更请求解决时长数据
    def load(
        self, org: str, repo: str
    ) -> DataloaderResult[ChangeRequestResolutionDurationData]:
        """
        加载特定组织和仓库的变更请求解决时长数据。

        参数:
        org (str): 组织名称。
        repo (str): 仓库名称。

        返回值:
        DataloaderResult[ChangeRequestResolutionDurationData]: 数据加载结果，
            成功时包含变更请求解决时长数据，失败时提供错误描述。
        """
        # 尝试获取仓库的变更请求解决时长数据
        data = get_repo_data(org, repo, ChangeRequestResolutionDurationData.name)
        if data is None:
            # 如果无法获取数据，返回失败结果
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )

        # 如果成功获取数据，返回数据加载成功结果
        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=ChangeRequestResolutionDurationData(
                value=load_non_trival_indicator_data(data),  # 加载具体的指标数据
            ),
            desc="",
        )



@register_dataloader
class ChangeRequestAgeRepoDataloader(BaseRepoDataloader):
    """
    用于加载更改请求年龄数据的仓库数据加载器类。

    属性:
    name (str): 数据加载器的名称。
    indicator_type (str): 指标类型，此处为"metric"。
    introducer (str): 指标的引入者，此处为"CHAOSS"。
    demo_url (str): 指标数据的演示URL。
    """

    name = "change_request_age"
    indicator_type = "metric"
    introducer = "CHAOSS"
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/change_request_age.json"

    def load(self, org: str, repo: str) -> DataloaderResult[ChangeRequestAgeData]:
        """
        加载指定组织和仓库的更改请求年龄数据。

        参数:
        org (str): 组织名称。
        repo (str): 仓库名称。

        返回:
        DataloaderResult[ChangeRequestAgeData]: 加载结果，包含成功标志、数据加载器实例、数据（如果成功）和描述信息。
        """
        # 尝试获取仓库的更改请求年龄数据
        data = get_repo_data(org, repo, ChangeRequestAgeData.name)
        if data is None:
            # 如果无法获取数据，返回失败结果
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",
            )

        # 如果成功获取数据，返回成功结果和加载的数据
        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=ChangeRequestAgeData(
                value=load_non_trival_indicator_data(data),
            ),
            desc="",
        )



# 注册为数据加载器的类，用于获取活动详情数据
@register_dataloader
class ActivityDetailRepoDataloader(BaseRepoDataloader):
    # 类属性定义
    name = "activity_detail"  # 数据加载器的名称
    indicator_type = "metric"  # 指标类型
    introducer = "X-lab"  # 数据提供者
    demo_url = "https://oss.x-lab.info/open_digger/github/X-lab2017/open-digger/activity_details.json"  # 示例数据URL

    # 加载指定组织和仓库的活动详情数据
    def load(self, org: str, repo: str) -> DataloaderResult[ActivityDetailData]:
        """
        加载指定组织和仓库的活动详情数据

        参数:
        org (str): 组织名称
        repo (str): 仓库名称

        返回值:
        DataloaderResult[ActivityDetailData]: 数据加载结果，成功时包含活动详情数据，失败时提供错误描述
        """
        # 尝试获取仓库的活动数据
        data = get_repo_data(org, repo, ActivityDetailData.name)
        if data is None:
            # 如果无法获取数据，返回失败结果
            return DataloaderResult(
                is_success=False,
                dataloader=t.cast("DataloaderProto", self),
                data=None,
                desc="Cannot find data for this indicator",  # 无法找到指标数据的错误描述
            )
        # 成功获取数据，返回数据加载结果
        return DataloaderResult(
            is_success=True,
            dataloader=t.cast("DataloaderProto", self),
            data=ActivityDetailData(
                value=load_base_data(
                    data, lambda x: [load_name_and_value(i) for i in x]  # 加载并转换数据格式
                ),
            ),
            desc="",  # 成功时的描述为空
        )

