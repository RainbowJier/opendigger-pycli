import typing as t

import requests

_GITHUB_API_BASE_URL = "https://api.github.com"


class RepoInfoType(t.TypedDict):
    repository: str
    repository_url: str
    owner_url: str
    is_fork: str
    created_at: str
    updated_at: str


class UserInfoType(t.TypedDict):
    username: str
    name: str
    email: str
    github_homepage_url: str
    created_at: str
    updated_at: str


class IssueInfoType(t.TypedDict):
    org_name: str
    repo_name: str
    issue_number: int
    issue_title: str
    issue_api_url: str
    issue_html_url: str


class IssueCommentInfoType(t.TypedDict):
    issue_comment_api_url: str
    body: str


def get_repo_info(
    org_name: str, repo_name: str, github_pat: t.Optional[str] = None
) -> t.Tuple[bool, RepoInfoType]:
    """
    Get repo info from GitHub API
    """
    url = f"{_GITHUB_API_BASE_URL}/repos/{org_name}/{repo_name}"

    if github_pat is not None:
        response = requests.get(
            url,
            headers={"Authorization": f"token {github_pat}"},
        )
    else:
        response = requests.get(url)

    if response.status_code != 200:
        return False, RepoInfoType(
            repository=f"{org_name}/{repo_name}",
            repository_url=f"https://www.github.com/{org_name}/{repo_name}",
            owner_url="null",
            is_fork="null",
            created_at="null",
            updated_at="null",
        )

    data = response.json()
    return True, RepoInfoType(
        repository=f"{org_name}/{repo_name}",
        repository_url=f"https://www.github.com/{org_name}/{repo_name}",
        owner_url=data["owner"]["html_url"],
        is_fork=str(data["fork"]),
        created_at=data["created_at"],
        updated_at=data["updated_at"],
    )


def get_user_info(
    username: str, github_pat: t.Optional[str] = None
) -> t.Tuple[bool, UserInfoType]:
    url = f"{_GITHUB_API_BASE_URL}/users/{username}"

    if github_pat is not None:
        response = requests.get(url, headers={"Authorization": f"token {github_pat}"})
    else:
        response = requests.get(url)

    if response.status_code != 200:
        return False, UserInfoType(
            username=username,
            name="null",
            email="null",
            github_homepage_url=f"https://www.github.com/{username}",
            created_at="null",
            updated_at="null",
        )

    data = response.json()
    return True, UserInfoType(
        username=username,
        name=data["name"],
        email=data["email"] if data["email"] is not None else "null",
        github_homepage_url=data["html_url"],
        created_at=data["created_at"],
        updated_at=data["updated_at"],
    )


def create_issue(
    org_name: str,
    repo_name: str,
    github_pat: str,
    title: str,
    body: t.Optional[str] = None,
    labels: t.Optional[t.List[str]] = None,
    assignees: t.Optional[t.List[str]] = None,
) -> t.Tuple[bool, t.Optional[IssueInfoType]]:
    """
    创建一个GitHub仓库的问题（issue）。

    参数:
    org_name (str): 组织名称。
    repo_name (str): 仓库名称。
    github_pat (str): GitHub个人访问令牌（PAT），用于授权。
    title (str): 问题标题。
    body (Optional[str]): 问题正文，默认为None。
    labels (Optional[List[str]]): 问题标签列表，默认为None。
    assignees (Optional[List[str]]): 问题分配给的用户列表，默认为None。

    返回值:
    Tuple[bool, Optional[IssueInfoType]]: 创建成功返回(True, IssueInfoType对象)，失败返回(False, None)。
    IssueInfoType包含问题的详细信息。

    """

    # 构建GitHub API的URL
    url: str = f"{_GITHUB_API_BASE_URL}/repos/{org_name}/{repo_name}/issues"

    # 准备提交给API的基本数据
    data: t.Dict[str, t.Union[str, t.List[str], int]] = {
        "title": title,
    }

    # 如果提供了标签、分配者或正文，则添加到数据中
    if labels:
        data["labels"] = labels
    if assignees:
        data["assignees"] = assignees
    if body:
        data["body"] = body

    # 使用requests库发送POST请求创建问题
    response = requests.post(
        url=url,
        headers={"Authorization": f"token {github_pat}"},
        json=data,
    )

    # 检查响应状态，成功时解析返回信息
    if response.status_code == 201:
        dat = response.json()
        return True, IssueInfoType(
            org_name=org_name,
            repo_name=repo_name,
            issue_number=dat["number"],
            issue_title=dat["title"],
            issue_api_url=dat["url"],
            issue_html_url=dat["html_url"],
        )

    # 请求失败时返回False和None
    return False, None



def create_issue_comment(issue_api_url: str, body: str, github_pat: str) -> bool:
    """
    向指定的GitHub问题接口发送POST请求，以添加一个新的评论。

    参数:
    issue_api_url (str): 问题的API URL，用于指定到哪个问题添加评论。
    body (str): 要添加的评论的内容。
    github_pat (str): GitHub的个人访问令牌（PAT），用于授权请求。

    返回:
    bool: 请求成功（状态码201）时返回True，否则返回False。
    """
    # 使用提供的个人访问令牌向指定的问题API URL发送评论内容
    response = requests.post(
        url=f"{issue_api_url}/comments",
        json={"body": body},
        headers={"Authorization": f"token {github_pat}"},
    )

    # 根据响应状态码判断请求是否成功，并返回相应的布尔值
    return response.status_code == 201



def create_issue_comment_reactions(
    issue_cooment_api_url: str,
    content: t.Literal[
        "+1", "-1", "laugh", "confused", "heart", "hooray", "rocket", "eyes"
    ],
    github_pat: str,
) -> bool:
    """
    向指定的GitHub问题评论添加表情反应。

    参数:
    issue_cooment_api_url (str): 问题评论的API URL，用于指定要添加反应的评论。
    content (t.Literal["+1", "-1", "laugh", "confused", "heart", "hooray", "rocket", "eyes"]): 表情反应的内容，限定为GitHub支持的特定表情。
    github_pat (str): GitHub的个人访问令牌（PAT），用于授权API请求。

    返回:
    bool: 请求是否成功。如果成功，返回True；否则返回False。
    """
    url = f"{issue_cooment_api_url}/reactions"  # 构造添加反应的API URL

    # 向API发送POST请求，添加表情反应
    response = requests.post(
        url=url,
        json={"content": content},
        headers={"Authorization": f"token {github_pat}"},
    )

    # 根据HTTP响应状态码判断请求是否成功，并返回结果
    return response.status_code == 200



def get_issue_comments(
    issue_api_url: str, github_pat: str
) -> t.Tuple[bool, t.List[IssueCommentInfoType]]:
    """
    获取给定问题的评论列表。

    参数:
    issue_api_url (str): 问题的API URL，用于获取评论。
    github_pat (str): GitHub的个人访问令牌（PAT），用于授权请求。

    返回:
    tuple: 包含一个布尔值和一个列表。布尔值表示请求是否成功，列表包含IssueCommentInfoType类型的对象，每个对象代表一个评论。
    """
    # 发起GET请求获取问题的评论列表
    response = requests.get(
        f"{issue_api_url}/comments", headers={"Authorization": f"token {github_pat}"}
    )

    # 检查请求是否成功
    if response.status_code != 200:
        return False, []

    # 解析响应体，将每个评论数据转换为IssueCommentInfoType对象，并存储到列表中
    body_datum = []
    datum = response.json()
    for dat in datum:
        body_datum.append(
            IssueCommentInfoType(
                body=dat["body"],
                issue_comment_api_url=f"{issue_api_url.rsplit('/', 1)[0]}/comments/{dat['id']}",
            )
        )

    return True, body_datum



def get_issue_comment_api_url(
    org_name: str, repo_name: str, issue_number: int, comment_number: int) -> str:
    """
    构建并返回特定GitHub仓库中问题（issue）评论的API URL。

    参数:
    org_name (str): 组织或个人的GitHub仓库所有者的名称。
    repo_name (str): GitHub仓库的名称。
    issue_number (int): 问题的编号。
    comment_number (int): 评论的编号。

    返回值:
    str: 指定问题评论的完整API URL。
    """
    # 格式化字符串，生成GitHub API的URL路径
    return f"{_GITHUB_API_BASE_URL}/repos/{org_name}/{repo_name}/issues/{issue_number}/comments/{comment_number}"


def search_issue_title(
    org_name: str,
    repo_name: str,
    title: str,
    labels: t.Optional[t.List[str]],
    github_pat: str,
) -> t.Tuple[bool, t.Optional[t.List[IssueInfoType]]]:
    """
    搜索给定组织和仓库中与指定标题和标签匹配的问题。

    参数:
    org_name (str): 组织名称。
    repo_name (str): 仓库名称。
    title (str): 问题标题。
    labels (t.Optional[t.List[str]]): 问题标签列表，可选。
    github_pat (str): GitHub个人访问令牌。

    返回:
    t.Tuple[bool, t.Optional[t.List[IssueInfoType]]]: 搜索结果布尔值（成功为True，失败为False）和问题信息列表（如果存在）。
    """
    # 构建GitHub搜索问题的API URL
    url = f"{_GITHUB_API_BASE_URL}/search/issues"

    # 构建查询字符串，包括问题标题、仓库名称和问题状态
    query_str = f"{title} repo:{org_name}/{repo_name} is:issue"

    # 如果提供了标签列表，则在查询字符串中添加标签条件
    if labels is None:
        labels = []
    for label in labels:
        query_str += f" label:{label}"

    # 发起GET请求，搜索问题
    response = requests.get(
        url=url,
        params={"q": query_str},
        headers={"Authorization": f"token {github_pat}"},
    )

    # 检查HTTP响应状态，如果不为200，则返回失败标志和None
    if response.status_code != 200:
        return False, None

    # 解析响应的JSON数据
    datum = response.json()

    # 遍历搜索结果，筛选出与指定标题匹配的问题，并填充问题信息列表
    issue_infos = []
    for dat in datum["items"]:
        if dat["title"] != title:
            continue
        issue_infos.append(
            IssueInfoType(
                org_name=org_name,
                repo_name=repo_name,
                issue_number=dat["number"],
                issue_title=dat["title"],
                issue_api_url=dat["url"],
                issue_html_url=dat["html_url"],
            )
        )

    # 如果未找到匹配的问题，则返回失败标志和None
    if not issue_infos:
        return False, None

    # 返回成功标志和问题信息列表
    return True, issue_infos
