import codecs
import re
import numpy as np
import pymysql
from snownlp import SnowNLP
import matplotlib.pyplot as plt
from snownlp import sentiment
from snownlp.sentiment import Sentiment

comment = []
with open('AvengersInfinityWar_new.csv', mode='r', encoding='utf-8') as f:
    rows = f.readlines()
    for row in rows:
        if row not in comment:
            comment.append(row.strip(',')[5])

def snowanalysis(self):
    sentimentslist = []
    for li in self:
        print(li)
        s = SnowNLP(li)
        print(s.sentiments)
        sentimentslist.append(s.sentiments)
    plt.hist(sentimentslist, bins=np.arange(0, 1.01, 0.01))
    plt.title('AvengersInfinityWar Sentiment Analysis')
    plt.xlabel('Sentiment Score from 0 to 1')
    plt.ylabel('Numbers/Thousand')
    plt.show()

snowanalysis(comment)