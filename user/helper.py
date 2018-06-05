# coding: utf-8
from django.shortcuts import render, redirect


def login_required(view_func):
    def check(request):
        if request.session.get('uid'):
            # 如果存在 uid，一切正常
            return view_func(request)
        else:
            # 如果不存在，跳转到登录页面
            return redirect('/user/login/')
    return check
