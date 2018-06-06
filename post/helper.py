# coding: utf-8

from django.core.cache import cache


def page_cache(view_func):
    def wrap(request):
        # Key 的构造规则
        # 检查缓存中是否有结果
        # 如果没有，直接执行原函数
        # 如果有，直接返回缓存的 response
        response = view_func(request)
    return wrap
