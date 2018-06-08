# coding: utf-8
from django.shortcuts import render, redirect

from user.models import User


def login_required(view_func):
    def check(request):
        if request.session.get('uid'):
            # 如果存在 uid，一切正常
            return view_func(request)
        else:
            # 如果不存在，跳转到登录页面
            return redirect('/user/login/')
    return check


def check_perm(need_perm):
    def wrap1(view_func):
        def wrap2(request):
            # 获取当前用户
            uid = request.session['uid']
            user = User.objects.get(id=uid)

            # 检查权限
            if user.has_perm(need_perm):
                return view_func(request)
            else:
                return render(request, 'blockers.html')
        return wrap2
    return wrap1
