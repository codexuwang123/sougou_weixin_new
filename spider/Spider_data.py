#!/usr/bin/python
# -*- coding:UTF-8 -*-
# 文件名:Spider_data.py
# 创建日期:2022/3/10 10:23
# 作者:XU
# 联系邮箱:iswongx@163.com
import time

import requests
import re
from parse import format_base_spdb
import random
from to_sql import save_data_to_sql
from redis_client import redis_connect
from settings import ua
import json
from settings import set_

list = []

conn = redis_connect.Redis_connect()
s_data = save_data_to_sql.Save_score_to_sql()


# 主要爬虫方法
class Spider_desc_sougou_weixin():

    # 基本请求头配置
    def __init__(self, wd):
        self.uA = ua.get('user_agent')
        self.wd = wd
        # logging_.info('搜索引擎搜狗微信，正在爬取={}相关内容。'.format(self.wd))

    # 解析主函数
    def spider_sougou_weixin(self, page, list_redis,section_name, author, keyword=None):

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
            format_base_spdb.format_text(first_data_list=url_list, tittle_list=tittle_list, keyword=keyword,
                                         cookies=cookie, list_redis=list_redis,section_name=section_name, author=author)
            print(cookie, '==============')
        else:
            print(res.text)


# 主函数调用
def last_mains():
    # 数据库获取关键次列表
    keyword_list = s_data.get_keyword()
    if keyword_list:
        for i in keyword_list:
            list_redis = []
            dict_redis = {}
            dict_redis['book_name'] = i.get('search_keyword')
            section_name = i.get('section_name')
            author_name = i.get('author')
            print(dict_redis)
            for n in range(1, set_.get('max_page')):
                spider_self = Spider_desc_sougou_weixin(wd=i.get('search_keyword'))
                spider_self.spider_sougou_weixin(page=n, keyword=spider_self.wd, list_redis=list_redis,section_name=section_name,author=author_name)

            dict_redis['data'] = list_redis
            dict_ = json.dumps(dict_redis, ensure_ascii=False)
            print(dict_)
            conn.insert_data_redis(redis_key='sougou_weixin', values=dict_)
            print('redis 数据存放成功')
            # 更新爬虫状态
            s_data.undate_data(status_='1', keyword=i.get('search_keyword'))
        # 关闭数据库连接
        # s_data.close()
        # return keyword_list
    else:
        print('========温馨提示：没有有效关键词需要爬取=======')


if __name__ == '__main__':
    # 生产者模式 生产任务
    while True:
        last_mains()
        time.sleep(3)
