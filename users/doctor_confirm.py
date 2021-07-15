# -*- coding: utf-8 -*-
# @Time    : 2020/10/22 9:42
# @Author  : Fang Hanzheng
# @File    : doctor_confirm.py
# @Software: PyCharm
from django.shortcuts import redirect, render


def login_confirm(request, user_id, username):
    request.session['username'] = username
    request.session['doctor_id'] = user_id
    request.session['history'] = {}
    request.session['active'] = True


def clean_session(request):
    request.session.flush()


def verify_login(request):
    if request.session.get('active'):
        return True
    else:
        return False


def get_doctor_id(request):
    doctor_id = request.session.get('doctor_id')
    if doctor_id:
        return doctor_id
    else:
        return False
