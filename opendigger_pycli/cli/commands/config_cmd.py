import typing as t
from dataclasses import fields

import click
from click.shell_completion import CompletionItem

from opendigger_pycli.console import CONSOLE
from opendigger_pycli.config import ALL_CONFIGS

from ..base import pass_environment

if t.TYPE_CHECKING:
    from click.core import Context, Parameter

    from opendigger_pycli.datatypes.config import BaseConfig

    from ..base import Environment


def config_shell_completion(
    ctx: t.Optional["Context"], param: t.Optional["Parameter"], incomplete: str
) -> t.List[CompletionItem]:
    incomplete_splited = incomplete.rsplit(".", 1)[0]
    if incomplete_splited == "":
        return [
            CompletionItem(config_dataclass_key) for config_dataclass_key in ALL_CONFIGS
        ]
    is_key = False
    last_config_dataclass: t.Optional[BaseConfig] = None
    for config_dataclass_key in ALL_CONFIGS:
        if incomplete_splited.startswith(config_dataclass_key):
            if incomplete_splited != config_dataclass_key:
                return [CompletionItem(config_dataclass_key + ".")]
            else:
                is_key = True
                last_config_dataclass = ALL_CONFIGS[config_dataclass_key]  # type: ignore
                break
        else:
            continue

    if not is_key and last_config_dataclass is None:
        return []

    if incomplete[:-1] == incomplete_splited:
        return [CompletionItem(f"{incomplete_splited}.{field.name}") for field in fields(last_config_dataclass)]  # type: ignore

    for field in fields(last_config_dataclass):  # type: ignore
        if incomplete in f"{incomplete_splited}.{field.name}":
            return [CompletionItem(f"{incomplete_splited}.{field.name}")]

    return []


def parse_config_key(key: str) -> t.Tuple[str, str]:
    section_name, config_key = key.rsplit(".", 1)
    return section_name, config_key


def check_config_setting(
    ctx: "Context", param: "Parameter", values: t.List[t.Tuple[str, str]]
) -> t.List[t.Tuple[str, str]]:
    for value in values:
        try:
            section_name, config_key = parse_config_key(value[0])
        except Exception:
            raise click.BadParameter(f"{value[0]} is not a valid config key")
        else:
            if section_name not in ALL_CONFIGS or config_key not in [
                field.name for field in fields(ALL_CONFIGS[section_name])
            ]:
                raise click.BadParameter(f"{value[0]} is not a valid config key")
    return values

"""
定义一个命令行接口，用于设置配置项。

参数:
- set: 用于设置配置项的命令行选项。接受多个键值对，每个键值对由`<CONFIG_KEY CONFIG_VALUE>`分隔。
  --set, -s: 可以使用长选项`--set`或者短选项`-s`来触发此功能。
  config_settings: 存储配置项键值对的参数名。
  type=(str, str): 确定参数类型，期望每个配置项键值对都是由两个字符串组成。
  multiple=True: 允许传入多个配置项键值对。
  callback=check_config_setting: 一个回调函数，用于检查配置项的有效性。
  shell_complete=config_shell_completion: 为这个选项启用shell自动完成功能。
  help="Set config value": 显示给用户的帮助信息。
  metavar="<CONFIG_KEY CONFIG_VALUE>": 指定命令行参数的显示名称。
"""
@click.command("config")  # type: ignore
@click.option(
    "--set",
    "-s",
    "config_settings",  # 存储配置项键值对的参数名。
    type=(str, str),
    multiple=True,
    callback=check_config_setting,
    shell_complete=config_shell_completion,
    help="Set config value",
    metavar="<CONFIG_KEY CONFIG_VALUE>",
)


@pass_environment
def config(
    env: "Environment",
    config_settings: t.List[t.Tuple[str, str]],
) -> None:
    """
       设置配置值

       参数:
       - env: "Environment"，环境对象，用于访问和修改配置
       - config_settings: t.List[t.Tuple[str, str]]，一个包含配置键值对的列表

       返回值:
       - None
       """
    # 如果没有配置设置，则打印当前配置并返回
    if not config_settings:
        CONSOLE.print(env.cli_config)
        return

    # 遍历配置设置列表，设置每个配置项
    for config_setting in config_settings:
        key, value = config_setting
        section_name, key = parse_config_key(key)
        env.dlog(f"set config: {section_name}.{key}={value}")
        env.set_config(section_name, key, value)
        env.dlog(f"finished to set config: {section_name}.{key}={value}")

    # 打印成功消息和当前配置
    CONSOLE.print("[green]Config set successfully[/]")
    CONSOLE.print(env.cli_config)
