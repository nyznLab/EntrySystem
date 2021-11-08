#!/usr/bin/env python
# *_*coding:utf-8 *_*
import json

from django.http import HttpResponse


class JsonUtil:
    success_message = '操作成功'
    error_message = '操作失败'

    @classmethod
    def success(self, data = {}, count = 0, message = '', code = 0):
        if message == '':
            message = self.success_message
        json_data = {
            'code': code,
            'message': message,
            'count': count,
            'data': data,
        }
        return HttpResponse(json.dumps(json_data))

    @classmethod
    def error(self, data = {}, count = 0, message = '', code = 1):
        if message == '':
            message = self.error_message
        json_data = {
            'code': code,
            'message': message,
            'count': count,
            'data': data,
        }
        return HttpResponse(json.dumps(json_data))
