from click.testing import CliRunner

from opendigger_pycli.cli import opendigger


def test_query():
    """
    测试查询命令的功能。

    该函数模拟用户通过命令行工具执行查询操作，针对特定的仓库进行查询，并验证查询结果是否符合预期。

    参数:
    无

    返回值:
    无
    """
    # 创建一个命令行运行器
    runner = CliRunner()
    # 使用指定参数调用opendigger命令，并捕获执行结果
    result = runner.invoke(
        opendigger, ["repo", "-r", "X-lab2017/open-digger", "query"]  # 执行查询命令
    )
    # 打印查询结果
    print(result.output)
    # 验证查询命令执行是否成功
    assert result.exit_code == 0


if __name__ == '__main__':
    test_query()