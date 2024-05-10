from click.testing import CliRunner

from opendigger_pycli.cli import opendigger


def test_repo_name_type():
    """
    测试仓库名称的类型检查。
    该函数无参数和返回值。
    """

    # 使用正确的仓库名称进行测试
    test_true_repo = "RainbowJier/Linux"
    runner = CliRunner()
    result = runner.invoke(
        opendigger, ["repo", "--repo", test_true_repo]
    )
    print(result.output)
    # 验证使用正确仓库名称的命令执行结果
    assert result.exit_code == 0

    # 使用错误格式的仓库名称进行测试
    test_false_repo = "opendigger\\opendigger"
    result = runner.invoke(
        opendigger, ["repo", "--repo", test_false_repo]
    )
    # 验证使用错误格式仓库名称的命令执行结果
    assert result.exit_code == 2

    # 使用不存在的仓库名称进行测试
    test_non_existing_repo = "opendigger/opendigger"
    result = runner.invoke(
        opendigger, ["repo", "--repo", test_non_existing_repo]
    )
    # 验证使用不存在仓库名称的命令执行结果
    assert result.exit_code == 2

if __name__ == '__main__':
    test_repo_name_type()
