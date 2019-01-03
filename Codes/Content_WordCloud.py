from wordcloud import WordCloud, STOPWORDS
import pandas as pd
import jieba
import matplotlib.pyplot as plt
import seaborn as sns
from pyecharts import Geo

f = open('\CSVData\AvengersInfinityWar_new.csv',encoding='UTF-8')
data = pd.read_csv(f,sep=',',header=None,encoding='UTF-8',names=['id','startTime','score','cityName','content'])

#分词
content = jieba.cut(str(data["content"]),cut_all=False)
wl_space_split= " ".join(content)
#导入背景图
backgroud_Image = plt.imread('background.png')
stopwords = STOPWORDS.copy()
print(" STOPWORDS.copy()",help(STOPWORDS.copy()))
#可以自行加多个屏蔽词，也可直接下载停用词表格
stopwords.add("电影")
stopwords.add("一部")
stopwords.add("一个")
stopwords.add("没有")
stopwords.add("什么")
stopwords.add("有点")
stopwords.add("这部")
stopwords.add("这个")
stopwords.add("不是")
stopwords.add("真的")
stopwords.add("感觉")
stopwords.add("觉得")
stopwords.add("还是")
stopwords.add("特别")
stopwords.add("非常")
stopwords.add("可以")
stopwords.add("因为")
stopwords.add("为了")
stopwords.add("比较")
stopwords.add("复制")
stopwords.add("粘贴")
stopwords.add("content")
stopwords.add("大家")
stopwords.add("你们")
stopwords.add("哈哈哈哈")
stopwords.add("哈哈哈")
stopwords.add("复制粘贴")
stopwords.add("object")
stopwords.add("评论")
stopwords.add("每天")


print (stopwords)
#设置词云参数
#参数分别是指定字体/背景颜色/最大的词的大小,使用给定图作为背景形状
wc =WordCloud(width=4000,height=3000,background_color='white',
              mask = backgroud_Image,font_path='C:/Windows/Fonts/simkai.ttf',
              stopwords=stopwords,max_font_size=450,
              random_state=100)
#将分词后数据传入云图
wc.generate_from_text(wl_space_split)
plt.imshow(wc)
plt.axis('off')#不显示坐标轴
plt.show()
#保存结果到本地
wc.to_file(r'\Results\AvengersInfinityWarWordCloud.jpg')


