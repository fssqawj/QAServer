# coding: utf-8


def is_lower_alpha(x):
    return '\u0061' <= x <= '\u007A'


def is_upper_alpha(x):
    return '\u0041' <= x <= '\u005A'


def is_number(x):
    return '\u0031' <= x <= '\u0039'


def is_simply_chinese(x):
    return '\u4e00' <= x <= '\u9fff'


def is_punctuation_or_unreadable(x):
    return not (is_lower_alpha(x)
                or is_number(x)
                or is_upper_alpha(x)
                or is_simply_chinese(x))
