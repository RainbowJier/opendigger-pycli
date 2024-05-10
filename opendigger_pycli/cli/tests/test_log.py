from click.testing import CliRunner

from opendigger_pycli.cli import opendigger


def test_log():
    """
    默认无参数配置
    """
    # 创建一个命令行运行器
    runner = CliRunner()
    # 使用指定参数调用opendigger命令，并捕获执行结果
    result = runner.invoke(
        opendigger, ["-L","DEBUG","repo","-r","RainbowJier/Linux"]  # 执行查询命令
    )
    # 打印查询结果
    print(result.output)
    # 验证查询命令执行是否成功
    assert result.exit_code == 0


if __name__ == '__main__':
    test_log()