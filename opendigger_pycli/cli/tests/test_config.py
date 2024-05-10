from click.testing import CliRunner

from opendigger_pycli.cli import opendigger


def test_config():
    """
    默认无参数配置
    """
    # 创建一个命令行运行器
    runner = CliRunner()
    # 使用指定参数调用opendigger命令，并捕获执行结果
    result = runner.invoke(
        opendigger, ["config"]  # 执行查询命令
    )
    # 打印查询结果
    print(result.output)
    # 验证查询命令执行是否成功
    assert result.exit_code == 0

def test_config_github_pat():
    """
    配置参数
    """
    # 创建一个命令行运行器
    runner = CliRunner()
    # 使用指定参数调用opendigger命令，并捕获执行结果
    result = runner.invoke(
        opendigger, ["config","--set","app_keys.github_pat","test_github_pat"]  # 执行查询命令
    )
    # 打印查询结果
    print(result.output)
    # 验证查询命令执行是否成功
    assert result.exit_code == 0


def test_config_openai_api_key():
    """
    配置参数
    """
    # 创建一个命令行运行器
    runner = CliRunner()
    # 使用指定参数调用opendigger命令，并捕获执行结果
    result = runner.invoke(
        opendigger, ["config","--set","app_keys.openai_key","test_openai_api_key"]  # 执行查询命令
    )
    # 打印查询结果
    print(result.output)
    # 验证查询命令执行是否成功
    assert result.exit_code == 0


if __name__ == '__main__':
    test_config()
    # test_config_github_pat()
    # test_config_openai_api_key()