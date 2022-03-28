#!/usr/bin/python
# -*- coding:UTF-8 -*-
# 文件名:settings.py
# 创建日期:2022/3/10 10:18
# 作者:XU
# 联系邮箱:iswongx@163.com


import time
import logging
import re


# 万能请求头格式化
def set_headers(string_new):
    '''

    :param string_new: 需要被格式化的请求头
    :return: None
    '''

    pattern = '^(.*?):(.*)$'
    for line in string_new.splitlines():
        print(re.sub(pattern, '\'\\1\':\'\\2\',', line).replace(' ', ''))


# 爬虫程序请求头集合

ua = {
    'user_agent': [
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1467.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1500.55 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.14 (KHTML, like Gecko) Chrome/24.0.1292.0 Safari/537.14',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
        'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20130401 Firefox/31.0',
        'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20120101 Firefox/29.0',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/29.0',
        'Mozilla/5.0 (Windows NT 6.1; rv:27.3) Gecko/20130101 Firefox/27.3',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:27.0) Gecko/20121011 Firefox/27.0',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0',
        'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0',
        'Mozilla/5.0 (Windows NT 6.2; rv:22.0) Gecko/20130405 Firefox/23.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:23.0) Gecko/20131011 Firefox/23.0',
        'Mozilla/5.0 (Windows NT 6.2; rv:22.0) Gecko/20130405 Firefox/22.0',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:22.0) Gecko/20130328 Firefox/22.0',
        'Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20130405 Firefox/22.0',
        'Mozilla/5.0 (Microsoft Windows NT 6.2.9200.0); rv:22.0) Gecko/20130405 Firefox/22.0',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/21.0.1',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/21.0.1',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:21.0.0) Gecko/20121011 Firefox/21.0.0',
        'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20130514 Firefox/21.0',
        'Mozilla/5.0 (Windows NT 6.2; rv:21.0) Gecko/20130326 Firefox/21.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130401 Firefox/21.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130331 Firefox/21.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130330 Firefox/21.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0',
        'Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20130401 Firefox/21.0',
        'Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20130328 Firefox/21.0',
        'Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20100101 Firefox/21.0',
        'Mozilla/5.0 (Windows NT 5.1; rv:21.0) Gecko/20130401 Firefox/21.0',
        'Mozilla/5.0 (Windows NT 5.1; rv:21.0) Gecko/20130331 Firefox/21.0',
        'Mozilla/5.0 (Windows NT 5.1; rv:21.0) Gecko/20100101 Firefox/21.0',
        'Mozilla/5.0 (Windows NT 5.0; rv:21.0) Gecko/20100101 Firefox/21.0',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64;) Gecko/20100101 Firefox/20.0',
        'Mozilla/5.0 (Windows x86; rv:19.0) Gecko/20100101 Firefox/19.0',
        'Mozilla/5.0 (Windows NT 6.1; rv:6.0) Gecko/20100101 Firefox/19.0',
        'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/18.0.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0)  Gecko/20100101 Firefox/18.0',

    ]}

# 正式库地址
true_sql = {
    'host': '',
    'port': 3306,
    'user': '',
    'password': '',
    'db': ''
}
# 测试库地址
test_sql = {
    'host': 'rm-2ze7q160da69ezjdnxo.mysql.rds.aliyuncs.com',
    'port': 3306,
    'user': 'pythonr_eptile',
    'password': '1qaz@WSX#EDC',
    'db': 'pythonr_eptile'
}

# 测试redis库地址
test_redis = {

    'host': '127.0.0.1',
    'port': 6379,
    'user': '',
    'password': '123456',
    'db': 7
}

# 正式库redis地址
true_redis = {
    'host': '',
    'port': 6379,
    'user': '',
    'password': '',
    'db': ''
}



# 设置日志函数
def set_log():
    now = int(time.time())
    timeArray = time.localtime(now)
    otherStyleTime = time.strftime("%Y%m%d", timeArray)
    logger2 = logging.getLogger('mylogger2')
    logger2.setLevel(logging.DEBUG)
    if not logger2.handlers:
        fh = logging.FileHandler('../log/{}.txt'.format(otherStyleTime), 'a', encoding='utf-8')
        formatter = logging.Formatter(
            '%(asctime)s - %(filename)s - [line:%(lineno)d] - %(levelname)s - %(process)d - %(message)s')
        fh.setFormatter(formatter)
        logger2.addHandler(fh)
    return logger2


# 基础配置

set_ = {
    'max_page': 200,  # 最大页数 200

}

import requests


def het():
    url = 'https://weixin.sogou.com/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS-fbL6csnqlh3gsNIUK_NZH_qAKceItPo1qXa8Fplpd9FjOz1ivY4Y6Mmuz1UpTCJoo2oBLXAKXWXESfByjQ_sQJLHb_z9LGoGpPPzB4MDDgcguvvcidqb0vav-ms-W8ojCxBZ3OdkOUOvk0TD6XmF4yw4wZ3a2z-wDAlb70nDCEkdg2M-uTff-9aswpbQJisLZ0D0qNTX3q8Tinv-EM-Jyfxjh3za6jWA..&type=2&query=%E4%B8%80%E5%93%81%E6%AF%92%E5%A6%83&token=CB483ED4A9CE46BBCEC8173FCC35CB10CE6A7912623C11F5&k=49&h=K'
    headers = {
        'Cookie': 'IPLOC=11111; SUID=11; SUV=000; ABTEST=41; weixinIndexVisited=1; JSESSIONID=337689584; PHPSESSID=364467378828; SNUID=774992389287482782; ariaDefaultTheme=undefid',
        'Host': 'weixin.sogou.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        print(res.url)
        data = res.content.decode('utf-8')
        print(data)

# 'https://mp.weixin.qq.com/s?src=11&timestamp=1648103925&ver=3695&signature=ip1Vbl7RsJ5BhMHylUcfhsEcc5-THlkzWG4Vs*-wMnOJpK29KUUCfVXNriGqJgNwPqh4gHLj*3clgCUvOR2y7-xo5KlBbo6PGL-usu6tSiA4cMYy*Hq7qxA3NQ69LRwy&new=1'

        s = re.findall("url \+=.*?'(.*?)';",data,re.S)
        new_url = ''.join(s)
        print(new_url)



# het()

def get_detail():
    url = 'http://mp.weixin.qq.com/s?src=11&timestamp=1648103925&ver=3695&signature=ip1Vbl7RsJ5BhMHylUcfhsEcc5-THlkzWG4Vs*-wMnOJpK29KUUCfVXNriGqJgNwPqh4gHLj*3clgCUvOR2y7-xo5KlBbo6PGL-usu6tSiA4cMYy*Hq7qxA3NQ69LRwy&new=1'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'
    }
    res = requests.get(url,headers=headers)
    print(res.text)

# get_detail()


import pandas as pd
import re

list1 = []
def download_(img_url,url):

    headers = {
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'
    }

    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        # print(res.text)
        data = res.json()
        list = data.get('data').get('list')
        for i in list:
            dict = {}
            dict['search_img_url'] = img_url
            dict['img_result'] = i.get('thumbUrl')
            dict['img_detail'] = i.get('fromUrl')
            list1.append(dict)
        print(list1)


def data_excel(data,sheet_name):
    # 数据转存成表格
    df = pd.DataFrame(data)
    # 定义表格名称+也可以直接省去这一步
    writer = pd.ExcelWriter('img_data0.xlsx')
    list2 = ['search_img_url', 'img_result', 'img_detail']
    # list1 = ['id', 'name', 'number', 'english_score', 'zh_score', 'last_scroe']
    df.to_excel(excel_writer=writer, columns=list2, index=False,
                encoding='utf-8', sheet_name=sheet_name)
    writer.save()
    writer.close()


#
# data_excel(data=list1,sheet_name='1')



