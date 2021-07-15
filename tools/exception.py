#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：entry_system 
@File ：exception.py
@IDE  ：PyCharm 
@Author ：skj
@Date ：1/26/21 8:39 PM 
'''
class BussinessException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message