#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名: format_base_spdb.py
# 作者:WangXu
# 联系邮箱:iswongx@163.com

# 格式化基本信息
import random
import re
import uuid
import requests
import time
from to_sql import save_data_to_sql
from settings import set_log
from redis_client import redis_connect
import json
import urllib3
from spider import Spider_data
from settings import ua

urllib3.disable_warnings()
logging_ = set_log()
conn = redis_connect.Redis_connect()



# 获取真实页面方法
def get_true(url,session):

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
        'Cookie': session,
        'user-agent': random.choice(ua.get('user_agent')),
    }
    print('=============================当前正在进入：{} ===================================='.format(url))
    try:
        res = requests.get(url, headers=headers, timeout=20, verify=False)
        time.sleep(0.5)
        if res.status_code == 200:
            info = res.text
            char = re.findall('charset="{0,1}(.*?)"', info, re.S)
            if char:
                try:
                    info1 = res.content.decode(encoding='{}'.format(char[0].lower()))
                    return info1, res.url
                except Exception as e:
                    print(e, '异常编码了================')
                    return info, res.url
            else:
                logging_.info('编码异常-连接为{}，'.format(res.url))
                return '编码异常', res.url
        else:
            print('状态码异常返回数据', res.text)
            logging_.info('状态码/服务异常-被访问链接为{}，'.format(res.url))
            return '服务异常', res.url
    except Exception as e:
        print(e, '异常')
        headers1 = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate',
            'If-None-Natch': '',
            'If-Modified-Since': '',
            'user-agent': random.choice(ua.get('user_agent'))
        }
        print('进入重定向了======1111 主意呀=========')
        try:
            res = session.get(url, headers=headers1, timeout=20, verify=False)
            logging_.info('特殊异常{}，异常连接{}'.format(e, url))
            return res.text, url
        except Exception as e:
            print(e, '---------')
            return '超时', url


# 详情页解析
def format_data(data, dict):
    dict_details = {}
    # 作者名称
    author2 = re.findall('<meta property="og:article:author" content="(.*?)"/>', data, re.S)
    if author2:
        author = author2[0].replace('\n', '').strip()
        dict_details['author'] = author.strip()
    else:
        author3 = re.findall('<strong class="profile_nickname">(.*?)</strong>', data, re.S)
        if author3:
            dict_details['author'] = author3[0].replace('\n', '').strip()
        else:
            dict_details['author'] = ''

    # 主角(默认为空)
    protagonist = ''
    if '主角' in data:
        protagonist = re.findall('主角：(.*?)<', data)
        if protagonist:
            dict_details['protagonist'] = protagonist[0].strip()
        else:
            dict_details['protagonist'] = ''
    else:
        dict_details['protagonist'] = protagonist
    # 小说简介
    if '小说介绍' in data:
        new_str = data[data.find('小说介绍'):data.find('长按识别开始看')]
        comp = re.compile(r'<[^>]+>')
        str = re.sub(comp, '', new_str).replace('小说介绍', '').replace('\n', '').replace('↓', '').strip()
        dict_details['describe'] = str
    else:
        stri = re.findall('<div class="rich_media_content " id="js_content" style="visibility: hidden;">(.*?)</div>',
                          data, re.S)
        if stri:
            comp = re.compile(r'<[^>]+>')
            str = re.sub(comp, '', stri[0]).replace('&nbsp;', '').strip()
            if '小说简介' in str:
                new_str = str[str.find('小说简介')::].replace('小说简介', '').strip()
                dict_details['describe'] = new_str
            else:
                dict_details['describe'] = str

    # 章节标题
    tittle = re.findall('<h1 class="rich_media_title" id="activity-name">(.*?)</h1>', data, re.S)
    if tittle:
        dict_details['tittle'] = tittle[0].replace('\n','').strip()
    else:
        dict_details['tittle'] = ''
    dict['details'] = dict_details


# 首页数据解析
def format_text(first_data_list, tittle_list, keyword,cookies):
    list = []
    cookies1 = cookies
    for i, n in zip(first_data_list, tittle_list):
        number = str(uuid.uuid1()).replace('-', '')
        dict = {}
        if 'http:' in i:
            i = i
        else:
            i = 'https://weixin.sogou.com' + i

        n = n.replace('&rdquo;', '').replace('red', '').replace('beg', '').replace('<em>', '').replace('end',
                                                                                                       '').replace(
            '&ldquo;', '').replace(
            '<!--_-->', '').replace('\r\n', '').replace('</em>','').strip()

        # 更进一步解析获取的脏数据
        new_url = i
        dict['number'] = number
        dict['tittle'] = n
        # 跳转链接
        dict['url'] = new_url
        # 真实链接
        dict['true_url'] = ''
        dict['keyword'] = keyword
        dict['cookies'] = cookies1
        dict_ = json.dumps(dict)
        print(dict_, '===========')
        conn.insert_data_redis(redis_key='sougou_weixin', values=dict_)


# 获取jsessionid
def get_jsessionid():
    url = 'https://weixin.sogou.com/websearch/wexinurlenc_sogou_profile.jsp'
    headers = {
        'user-agent': random.choice(ua.get('user_agent'))
    }
    resss = requests.get(url, headers=headers)
    cookie = ''
    for k, v in resss.cookies.items():
        cookie = cookie + k + '=' + v + ';'
    return cookie


# 搜狗获取真是链接程序
def get_sougou_weixin_rue_url(skip_url,session):
    headers = {
        'Cookie': session,
        'Host': 'weixin.sogou.com',
        'Connection': 'keep-alive',
        'User-Agent': random.choice(ua.get('user_agent'))
    }
    try:
        res = requests.get(skip_url, headers=headers, verify=False)
        if res.status_code == 200:
            data = res.content.decode('utf-8')
            data1 = re.findall("url \+=.*?'(.*?)';", data, re.S)
            if data1:
                new_url = ''.join(data1)
                print(new_url, '真实链接==1kokofklsflsk')
                return new_url
            else:
                data2 = res.text
                print(res.text,'000999999999999911111111111111111111111111')
                data3 = re.findall("url \+=.*?'(.*?)';", data2, re.S)
                if data3:
                    new_url3 = ''.join(data3)
                    print(new_url3, '真实链接==')
                    return new_url3
                else:
                    print(res.text)
                    print('1111111111111111111111111111111111111111111111 ')
        else:
            print(res.text)
            print('99999999999999999999999')
    except Exception as e:
        print(e, '真实连接')
        res = requests.get(skip_url, headers=headers, verify=False)
        if res.status_code == 200:
            info = res.text
            data1 = re.findall("URL='(.*?)'", info)
            if data1:
                return data1[0]
        return skip_url


# 主要解析程序
def get_():

    print('线程进来了================')
    dta = conn.search_data_redis(redis_key='sougou_weixin')
    if dta:
        dict = json.loads(dta)
        # print(dict,'000109q39q8989q')
        new_tittle = dict.get('tittle')
        new_url = dict.get('url')
        cookies = dict.get('cookies')
        # print(cookies,'---------------')
        cookies1 = get_jsessionid()
        # print(cookies1,'======================')
        print(type(new_url), new_url, '000000011111111111111111111111111')
        true_url1 = get_sougou_weixin_rue_url(skip_url=new_url,session=cookies+cookies1)
        details_data, true_url = get_true(url=true_url1,session=cookies+cookies1)
        dict['true_url'] = true_url
        new_keyword = dict.get('keyword')
        if new_keyword in new_tittle:
            if details_data == '编码异常':
                print('编码异常====', true_url)
                return None
            if details_data == '超时':
                print('超时了------------------', true_url)
                return None
            if details_data == '服务异常':
                print('服务异常=================', true_url)
                return None

            format_data(data=details_data, dict=dict)
            # 数据库存放数据
            sql_server = save_data_to_sql.Save_score_to_sql()
            sql_server.search_data_to_sql(data=dict)
            sql_server.details_data_to_sql(data=dict)
            # list.append(dict)
            # print(dict)
            return new_keyword
        else:
            print('不符合跳过0000000000000000000000000000000000')
            print(new_tittle, '111111111111111111')
            print(true_url, '2222222222222222')
    else:
        print('数据爬取完成====')


if __name__ == '__main__':

    # s = Spider_data.Spider_desc_sougou_weixin(wd='一品毒妃')
    # s.spider_sougou_weixin(page='1', keyword=s.wd)
    try:
        while True:
            get_()
            time.sleep(3)
    except KeyboardInterrupt as e:
        print(e, '强制中断 异常捕获===')
