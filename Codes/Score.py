# 导入Pie组件，用于生成饼图
from pyecharts import Pie


# 获取评论中所有评分
rates = []
with open('\CSVData\AvengersInfinityWar_new.csv', mode='r', encoding='utf-8') as f:
    rows = f.readlines()
    for row in rows:
        rates.append(row.split(',')[2])
print(rates)

# 定义星级，并统计各星级评分数量
attr = ['五星', '四星', '三星', '二星', '一星']
value = [
    rates.count('5') + rates.count('4.5'),
    rates.count('4') + rates.count('3.5'),
    rates.count('3') + rates.count('2.5'),
    rates.count('2') + rates.count('1.5'),
    rates.count('1') + rates.count('0.5')
]
print(value)

pie = Pie('评分星级比例', title_pos='center', width=1200)
pie.add(12-28, attr, value, center=[50, 50], is_random=True,
        radius=[30, 75], rosetype='area',
        is_legend_show=False, is_label_show=True)
pie.render('\Results\AvengersInfinityWar_new_评分.html')

