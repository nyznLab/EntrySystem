#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：tools
@File ：exception.py
@IDE  ：PyCharm
@Author ：skj
@Date ：6/1/21 1:31 PM
'''
import logging
class BussinessException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

# 处理异常
def handle_exception(e):
    logging.basicConfig(level=logging.ERROR,
                        filename='error.log',
                        filemode='a',
                        format='%(asctime)s - %(message)s')
    logging.error(e)
