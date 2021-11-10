#!/usr/bin/env python
# *_*coding:utf-8 *_*

from django import template

register = template.Library()


# 转为整型
@register.filter()
def to_int(value):
    return int(value)


# 转为字符串
@register.filter()
def to_str(value):
    return str(value)
