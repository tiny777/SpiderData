# 获取的评论可能有重复，为了最终统计的真实性，需做去重处理
def duplicateChecking(old,new):
    oldfile = open(old,'r',encoding='UTF-8')
    newfile = open(new,'w',encoding='UTF-8')
    content_list = oldfile.readlines() #读取的数据集
    content_alreadly_ditinct = [] #存储不重复的评论数据
    for line in content_list:
        if line not in content_alreadly_ditinct: #评论不重复
            newfile.write(line)
            content_alreadly_ditinct.append(line)


if __name__ == '__main__':
    duplicateChecking(r'AvengersInfinityWar.csv', r'AvengersInfinityWar_new.csv')