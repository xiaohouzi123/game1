# coding: utf-8

from django.core.cache import cache


def page_cache(timeout):
    def wrap1(view_func):
        def wrap2(request):
            # Key 的构造规则: view / vars / user
            key = 'PageCache-%s-%s' % (request.session.session_key, request.get_full_path())
            # print('key is :', key)
            response = cache.get(key)
            # print('get from cache', response)
            if response is None:
                # 如果没有，直接执行原函数
                response = view_func(request)
                # print('get from view', response)
                cache.set(key, response, timeout)
                # print('set to cache')
            return response
        return wrap2
    return wrap1
