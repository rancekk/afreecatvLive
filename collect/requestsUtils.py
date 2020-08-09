import requests
import json


class requestsUtils:
    proxies = {
        'http': '127.0.0.1:1081',
        'https': '127.0.0.1:1081'
    }

    def post_main(self, method, url, data, header):
        global res
        if method == "post":
            if header == "form-data":
                res = requests.post(url=url, data=data, proxies=self.proxies)

            if header == "Content-type:application/json":
                res = requests.post(url=url, json=data, proxies=self.proxies)
        return res.text

    def get_main(self, method, url):
        global res
        if method == "get":
            res = requests.get(url=url, proxies=self.proxies)
        return res.text
