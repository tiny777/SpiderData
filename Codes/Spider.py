#encoding='UTF-8'
from urllib import request
import json
import time
from datetime import datetime
from datetime import timedelta
import pandas as pd
from lxml import etree
from tqdm import tqdm
import random
import re
import csv


# 获取数据，根据url获取
def get_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
    }
    req = request.Request(url, headers=headers)
    response = request.urlopen(req)
    if response.getcode() == 200:
        return response.read()
    return None

# 处理数据
def parse_data(html):
    data = json.loads(html)['cmts']  # 将str转换为json
    comments = []
    for item in data:
        comment = {
            'id': item['id'],
            #'nickName': item['nickName'],
            'cityName': item['cityName'] if 'cityName' in item else '',  # 处理cityName不存在的情况
            # 处理评论内容换行的情况,并且将逗号替换为空格
            'content': item['content'].replace('”',' ').replace('“',' ').replace(',',' ').replace('，',' ').replace('\n', ' '),  
            'score': item['score'],
            'startTime': item['startTime']
        }
        comments.append(comment)
    return comments

# 存储数据，存储到文本文件
def savetoCSV():
    #设置指定时间向前爬取评论数据或者从特定的时间段爬取评论
    #start_time = '2015-05-12 02:40:34'
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 获取当前时间，从当前时间向前获取
    #设置爬取评论数据的截至时间
    end_time = '2018-08-01 00:00:00'
    while start_time > end_time:
        #雷神3 249894   
        #复联3 248170
        #复联2 78429
        #海王  249342
        #蚁人2 343208
        url = 'http://m.maoyan.com/mmdb/comments/movie/343208.json?_v_=yes&offset=0&startTime=' + start_time.replace(' ', '%20')
        html = None
        '''
            问题：当请求过于频繁时，服务器会拒绝连接，实际上是服务器的反爬虫策略
            解决：1.在每个请求间增加延时0.1秒，尽量减少请求被拒绝
                 2.如果被拒绝，则0.5秒后重试
        '''
        try:
            html = get_data(url)
        except Exception as e:
            time.sleep(0.5)
            html = get_data(url)
        else:
            time.sleep(0.1)

        comments = parse_data(html)
        print(comments)
        start_time = comments[14]['startTime']  # 获得末尾评论的时间
        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') + timedelta(seconds=-1)  # 转换为datetime类型，减1秒，避免获取到重复数据
        start_time = datetime.strftime(start_time, '%Y-%m-%d %H:%M:%S')  # 转换为str
        
        #将数据写入csv文件中
        for item in comments:
            with open('AntManAndtheWasp.csv', 'a', encoding='utf-8') as f:
                f.write(str(item['id']) + ',' + item['startTime'].strip('[\'').split(' ')[0] + ',' + str(item['score']) + ',' + item['cityName'] + ',' + str(item['content']) + '\n')
                #f.write(str(item['id'])+','+item['nickName'] + ',' + item['cityName'] + ',' + item['content'] + ',' + str(item['score'])+ ',' + item['startTime'] + '\n')
        


if __name__ == '__main__':
    html = get_data('http://m.maoyan.com/mmdb/comments/movie/343208.json?_v_=yes&offset=0&startTime=2019-01-04%2022%3A25%3A03')
    comments = parse_data(html)
    print(comments)
    savetoCSV()
