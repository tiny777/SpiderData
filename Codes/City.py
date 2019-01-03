import os
import pandas as pd
from pandas import DataFrame
import re
from pyecharts import Line, Geo, Bar, Pie, Page, ThemeRiver
from snownlp import SnowNLP
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

fth = open('pyecharts_citys_supported.txt', 'r', encoding='utf-8').read() # pyecharts支持城市列表

# 过滤字符串只保留中文
def translate(str):
    line = str.strip()
    p2 = re.compile('[^\u4e00-\u9fa5]')   #中文的编码范围是：\u4e00到\u9fa5
    zh = " ".join(p2.split(line)).strip()
    zh = ",".join(zh.split())
    str = re.sub("[A-Za-z0-9!！，%\[\],。]", "", zh)
    return str

def count_city(csv_file):
    path = os.path.abspath(os.curdir)
    csv_file = path+ "\\" + csv_file +".csv"
    csv_file = csv_file.replace('\\', '\\\\')
    
    d = pd.read_csv(csv_file, engine='python', encoding='utf-8')
    city = [translate(n) for n in d['cityName'].dropna()] # 清洗城市，将中文城市提取出来并删除标点符号等 
    
    #这是从网上找的省份的名称，将他转换成列表的形式
    province = '湖南,湖北,广东,广西、河南、河北、山东、山西,江苏、浙江、江西、黑龙江、新疆,云南、贵州、福建、吉林、安徽,四川、西藏、宁夏、辽宁、青海、甘肃、陕西,内蒙古、台湾,海南'
    province = province.replace('、',',').split(',')
    rep_province = "|".join(province) #re.sub中城市替换的条件
    
    All_city = jieba.cut("".join(city)) # 分词，将省份和市级地名分开，当然有一些如吉林长春之类没有很好的分开，因此我们需要用re.sub（）来将之中的省份去除掉
    final_city= []
    for a_city in All_city:
        a_city_sub = re.sub(rep_province,"",a_city) #对每一个单元使用sub方法，如果有省份的名称，就将他替换为“”（空）
        if a_city_sub == "": #判断，如果为空，跳过
            continue
        elif a_city_sub in fth: #因为所有的省份都被排除掉了，便可以直接判断城市在不在列表之中，如果在，final_city便增加
            final_city.append(a_city_sub)
        else: #不在fth中的城市，跳过
            continue
            
    result = {}
    print("城市总数量为：",len(final_city))
    for i in set(final_city):
        result[i] = final_city.count(i)
    return result


def draw_citys_pic(csv_file):
    page = Page(csv_file+":评论城市分析")
    info = count_city(csv_file)
    geo = Geo("","Ctipsy原创",title_pos="center", width=1200,height=600, background_color='#404a59', title_color="#fff")
    while True:   # 二次筛选，和pyecharts支持的城市库进行匹配，如果报错则删除该城市对应的统计
        try:
            attr, val = geo.cast(info)
            geo.add("", attr, val, visual_range=[0, 300], visual_text_color="#fff", is_geo_effect_show=False,
                    is_piecewise=True, visual_split_number=6, symbol_size=15, is_visualmap=True)
        except ValueError as e:
            e = str(e)
            e = e.split("No coordinate is specified for ")[1]  # 获取不支持的城市名称
            info.pop(e)
        else:
            break
    info = sorted(info.items(), key=lambda x: x[1], reverse=False)  # list排序
    # print(info)
    info = dict(info)   #list转dict
    # print(info)
    attr, val = [], []
    for key in info:
        attr.append(key)
        val.append(info[key])


    geo1 = Geo("", "评论城市分布", title_pos="center", width=3000, height=2000,
              background_color='#404a59', title_color="#fff")
    geo1.add("", attr, val, visual_range=[0, 3000], visual_text_color="#fff", is_geo_effect_show=False,
            is_piecewise=True, visual_split_number=10, symbol_size=15, is_visualmap=True, is_more_utils=True)
    geo1.render(csv_file + "_城市dotmap.html")
    
    page.add_chart(geo1)
    geo2 = Geo("", "评论来源热力图",title_pos="center", width=3000,height=2000, background_color='#404a59', title_color="#fff",)
    geo2.add("", attr, val, type="heatmap", is_visualmap=True, visual_range=[0, 1000],visual_text_color='#fff', is_more_utils=True)
    geo2.render(csv_file+"_城市heatmap.html")  # 取CSV文件名的前8位数
    
    page.add_chart(geo2)
    bar = Bar("", "评论来源排行", title_pos="center", width=1800, height=1200 )
    bar.add("", attr, val, is_visualmap=True, visual_range=[0, 100], visual_text_color='#fff',mark_point=["average"],mark_line=["average"],
            is_more_utils=True, is_label_show=True, is_datazoom_show=True, xaxis_rotate=45)
    bar.render(csv_file+"_城市评论bar.html")  # 取CSV文件名的前8位数
    
    page.add_chart(bar)
    pie = Pie("", "评论来源饼图", title_pos="right", width=5000, height=15000)
    pie.add("", attr, val, radius=[20, 50], label_text_color=None, is_label_show=True, legend_orient='vertical', is_more_utils=True, legend_pos='left')
    pie.render(csv_file + "_城市评论Pie.html")  # 取CSV文件名的前8位数
    
    page.add_chart(pie)
    page.render(csv_file + "_城市评论分析汇总.html")


if __name__ == '__main__':
    draw_citys_pic("\CSVData\AvengersInfinityWar_new")






