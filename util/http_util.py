# -*- coding: utf-8 -*-
# @Time: 2024/10/31 14:21
# @Author: Sui Yuan
# @Software: PyCharm
# @Desc:

import urllib3
import json


class HttpResult:
    def __init__(self, data):
        result = json.loads(data)
        if "code" in result:
            self.code = result["code"]
        elif "resultCode" in result:
            self.code = result["resultCode"]
        else:
            self.code = None

        if "message" in result:
            self.message = result["message"]
        elif "resultMsg" in result:
            self.message = result["resultMsg"]
        else:
            self.message = None

        self.tid = result["tid"] if "tid" in result else None
        self.data = result["data"] if "data" in result else None


class HttpClient:
    """
    http请求类，利用请求池
    """

    def __init__(self):
        self.__http = urllib3.PoolManager(num_pools=10)

    def do_get(self, url, headers=None, **kwargs):
        with self.__http.request('GET', url, preload_content=False, headers=headers, **kwargs) as response:
            return self._handle_response(response)

    def do_post(self, url, data=None, headers=None, **kwargs):
        with self.__http.request('POST', url, body=data, preload_content=False, headers=headers, **kwargs) as response:
            return self._handle_response(response)

    @staticmethod
    def _handle_response(response):
        data = response.data.decode()
        # status = response.status
        # reason = response.reason
        return HttpResult(data)


# 创建一个全局的实例
http_client = HttpClient()
