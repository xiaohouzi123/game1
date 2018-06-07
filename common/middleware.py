# coding: utf-8

import time

from django.utils.deprecation import MiddlewareMixin


def simple_middleware(get_response):
    '''简单装饰器'''
    print('do_something_for_init()')
    def middleware(request):
        print('do_something_before_views(request)')
        response = get_response(request)  # views 函数在这里执行
        print('do_something_after_views(response)')
        return response
    return middleware



class BlockMiddleware(MiddlewareMixin):
    '''
    限制用户的访问频率最大为每秒 2 次，超过 2 次时，等待至合理时间再返回

        1   1528331000.00
        2   1528331000.01
        3   1528331001.57
        --------------------- 前面的丢弃
        4   1528331001.93  <-
        5   1528331001.99
        --------------------- 前两次的时间
        6   1528331003.53  <-
    '''
    def process_request(self, request):
        current = time.time()
        request_time = request.session.get('request_time', [0, 0])  # 取出历史访问时间
        if (current - request_time[0]) < 1:  # 检查与最早的时间差是否小于 1s
            time.sleep(60)
            current = time.time()
        request.session['request_time'] = [request_time[1], current]  # 更新访问时间
