#-*-encoding:utf-8-*-

import  json
import matplotlib.pyplot as plt

startPath='F:/mystuff/GitHubRespository/pydata-book/'
path =startPath+ 'ch02/usagov_bitly_data2012-03-16-1331923249.txt'

fileContent = open(path).readline()
#print fileContent

#python内置json模块，将json字符串转换成python字典对象
records = [json.loads(line) for line in open(path)]     #列表推导式
#print records[0]
#print records[0]['tz']

time_zones = [rec['tz'] for rec in records if 'tz' in rec]
#print time_zones[:10]

#对时区进行计数，介绍两个方法：一个较难使用标准Python库，另一个较简单使用Pandas
def get_counts(sequence):
    counts ={}
    for x in sequence:
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1
    return  counts

from collections import  defaultdict
def get_counts2(sequence):
    counts = defaultdict(int) #所有的值均会被初始化为0
    for x in sequence:
        counts[x] += 1
    return  counts

counts = get_counts(time_zones)
#print counts['America/New_York']
#print len(time_zones)

#获取前10位的时区及其计数值，需要用到一些有关字典的处理技巧：
def top_counts(count_dict, n=10):
    value_key_pairs = [(count, tz) for tz, count in count_dict.items()]
    value_key_pairs.sort()
    return value_key_pairs[-n:]

#print top_counts(counts)

#用Pandas对时区进行计数
from pandas import DataFrame, Series
import pandas as pd; import numpy as np

frame = DataFrame(records)
#print frame
#print frame['tz'][:10]

tz_counts = frame['tz'].value_counts()  #frame['tz']所返回的Series对象的一个方法，可得到前边所需要的数据信息（对时区进行计数统计）
#print tz_counts[:10]    #输出时区计数的top10

clean_tz = frame['tz'].fillna('Missing')  #给你记录中未知或缺失的时区填上一个替代值。
clean_tz[clean_tz == ''] = 'Unknown'
#fillna函数可以替换缺失值（NA），而未知值（空字符串）则通过布尔类型数组索引加以替换
tz_counts = clean_tz.value_counts()
#print tz_counts[:10]

#利用tz_counts对象的plot方法可以得到一张水平条形图
tz_counts[:10].plot(kind='barh', rot=0)
#plt.show()

#print frame['a'][1]
#print frame['a'][50]
#print frame['a'][51]

#解析数据，通过Python内置的字符串函数和正则表达式
results = Series([x.split()[0] for x in frame.a.dropna()])
#print results[:5]
#假设想按Windows和非Windows用户对时区统计信息进行分解。为了简单只要agent字符串中含有windows就认为是windows用户
#由于有agent缺失，先从数据中移除：
cframe = frame[frame.a.notnull()]
operating_system = np.where(cframe['a'].str.contains('Windows'), 'Windows', 'Not Windows')
#print operating_system[:5]

#接下来根据时区和新得到的操作系统列表对数据进行分组：
by_tz_os = cframe.groupby(['tz', operating_system])
agg_counts = by_tz_os.size().unstack().fillna(0)   #通过size对分组结果进行计数（类似于上面的value_counts函数)，并利用unstack对计数结果进行重塑
print agg_counts[:10]

#最后，选取最常出现的时区。根据agg_counts中的行数构造了一个间接索引数组
indexer = agg_counts.sum(1).argsort()
print indexer[:10]

count_subset = agg_counts.take(indexer)[-10:]
print count_subset

#生成一张条形图。使用staked=True来生成一张堆积条形图
count_subset.plot(kind='barh', stacked=True)

#由于这张图不太容易看清楚较小分组中Windows用户的相对比例，因此可以将各行规范化为”总计为1“并重新绘图
normed_subset = count_subset.div(count_subset.sum(1), axis=0)
normed_subset.plot(kind='barh', stacked=True)
plt.show() #用plot画的图，在非IPython中得调用show方法才可以显示；