#!/usr/bin/python
# -*- coding:UTF-8 -*-
# 文件名:Spider_data.py
# 创建日期:2022/3/10 10:23
# 作者:XU
# 联系邮箱:iswongx@163.com

import requests
import re
from parse import format_base_spdb
from settings import set_log
import random

list = []
logging_ = set_log()

from settings import ua


# 主要爬虫方法
class Spider_desc_sougou_weixin():

    # 基本请求头配置
    def __init__(self, wd):
        self.uA = ua.get('user_agent')
        self.wd = wd
        logging_.info('搜索引擎搜狗微信，正在爬取={}相关内容。'.format(self.wd))

    # 解析主函数
    def spider_sougou_weixin(self, page, keyword=None):

        self.url = 'https://weixin.sogou.com/weixin?'
        self.params = {
            'query': keyword,
            '_sug_type_': '',
            'sut': '4803',
            'lkt': '1%2C1648087550294%2C1648087550294',
            's_from': 'input',
            'from': 'index-nologin',
            '_sug_': 'y',
            'type': '2',
            'sst0': '1648087550395',
            'suguuid': '8b531100-b520-4d21-8d9f-074d40f77c4f',
            'page': page,
            'ie': 'utf8',
            'w': '01019900',
            'dr': '1'
        }
        self.headers = {
            'User-Agent': random.choice(self.uA),
            'X-Requested-With': 'XMLHttpRequest'
        }
        res = requests.get(self.url, headers=self.headers, params=self.params, verify=False)
        if res.status_code == 200:
            cookie = ''
            for k, v in res.cookies.items():
                if k == 'SNUID':
                    cookie = cookie + k + '=' + v + ';'

            url_list = re.findall('<div class="txt-box">.*?<a target="_blank" href="(.*?)"', res.text, re.S)
            tittle_list = re.findall('uigs="article_title_\d+">(.*?)</a>', res.text, re.S)
            format_base_spdb.format_text(first_data_list=url_list, tittle_list=tittle_list, keyword=keyword,cookies = cookie)
            print(cookie,'==============')
        else:
            print(res.text)



