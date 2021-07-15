# -*- coding: utf-8 -*-
# @Time    : 2020/11/5 10:31
# @Author  : Fang Hanzheng
# @File    : MyMiddleware.py
# @Software: PyCharm
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, render
import time
from django.utils.deprecation import MiddlewareMixin
import re

# white_list = ['/login/', "/logout/"]

# 中间件 核对当前request中session的active是否为True
# 再添加一下doctor_id


class AuthMiddleWare(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        # 如果是访问白名单 则不需要验证 直接return
        destination_url = request.path_info
        if destination_url == '/':
            return
        # 如果访问的不是白名单 则需要验证active状态 True就什么都不做
        if request.session.get('active', False):
            return
        # active为未激活状态 重定向到登陆页面 返回错误信息
        else:
            error = 'You need to login first !'
            return redirect('/')


class PageRecordMiddleWare(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        full_url = request.get_full_path()
        # 不记录添加删除等操作的url
        current_time = time.time()
        if full_url.find('add', 0, len(full_url)) or full_url.find('del', 0, len(full_url)):
            return
        if not request.session.get('history'):
            request.session['history'] = {}
            request.session.get('history')[current_time] = full_url
        else:
            # 仅记录最近10次记录
            if len(request.session['history']) >= 10:
                history = request.session.get('history')
                history.pop(min(list(history.keys())))
                request.session['history'] = history
            request.session.get('history')[current_time] = full_url
        return
