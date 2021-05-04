import os
import re
from typing import Literal, Any
from html import unescape

patterns = ["title", "id", "name"]
PathPattern = Literal["title", "id", "name"]

_count: int = 0


def repair_filename(filename: str) -> str:
    """ 修复不合法的文件名 """

    def to_full_width_chr(matchobj: "re.Match[str]") -> str:
        char = matchobj.group(0)
        full_width_char = chr(ord(char) + ord("？") - ord("?"))
        return full_width_char

    # 路径非法字符，转全角
    regex_path = re.compile(r'[\\/:*?"<>|]')
    # 空格类字符，转空格
    regex_spaces = re.compile(r"\s+")
    # 不可打印字符，移除
    regex_non_printable = re.compile(
        r"[\001\002\003\004\005\006\007\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"
        r"\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a]"
    )

    # 由于部分内容可能是从 HTML 解析的，所以使用 html 反转义
    filename = unescape(filename)
    filename = regex_path.sub(to_full_width_chr, filename)
    filename = regex_spaces.sub(" ", filename)
    filename = regex_non_printable.sub("", filename)
    filename = filename.strip()
    if not filename:
        filename = "未命名文件_{:04}".format(_count)
        _count += 1
    return filename


def reslove_path_pattern(
    pattern_template: str, auto_pattern_template: str, pattern_dict: dict[PathPattern, Any]
) -> str:
    # 保证所有传进来的值都满足路径要求
    for key, value in pattern_dict.items():
        if isinstance(value, str):
            pattern_dict[key] = repair_filename(value)
    return pattern_template.format(auto=auto_pattern_template.format(**pattern_dict), **pattern_dict)


def reslove_path(dir: str, subpath: str) -> tuple[str, str]:
    """ 将目录与子路径拼接后重新分离为「目录路径」与「文件名」"""
    path = os.path.join(dir, subpath)
    return os.path.split(path)
