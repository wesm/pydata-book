# -*-coding:utf-8-*-
import json
from collections import defaultdict
from collections import Counter
from pandas import DataFrame,Series
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

path = './example.txt'
records = [json.loads(line) for line in open(path)]
time_zones = [rec['tz'] for rec in records if 'tz' in rec]

def get_counts(sequence): # 统计时区
    counts = {}
    for x in sequence:
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1
    return counts

def get_counts2(sequence): # 简易统计时区的方法
    counts = defaultdict(int)
    for x in sequence:
        counts[x] += 1
    return counts

def top_counts(count_dict,n=10): # 前10位时区及值
    value_key_pairs = [(count,tz) for tz,count in count_dict.items()]
    value_key_pairs.sort()
    return value_key_pairs[-10:]

# counts = Counter(time_zones) # 用Count方法统计



'''
用pandas对时区进行统计
'''

frame = DataFrame(records)
'''
clean_tz = frame['tz'].fillna('Missing')
clean_tz[clean_tz == ''] = 'Unknow'
tz_counts = clean_tz.value_counts()
pic = tz_counts[:10].plot(kind='barh',rot=0)
plt.show()
'''

'''
统计浏览器信息
results = Series([x.split()[0] for x in frame.a.dropna()])
print results.value_counts()[:8]
'''


cframe = frame[frame.a.notnull()]
operating_system = np.where(cframe['a'].str.contains('Windows'), 'Windows', 'Not Windows')
by_tz_os = cframe.groupby(['tz', operating_system])
agg_counts = by_tz_os.size().unstack().fillna(0)
indexer = agg_counts.sum(1).argsort()
count_subset = agg_counts.take(indexer)[-10:]
count_subset.plot(kind='barh',stacked=True)
normed_subset = count_subset.div(count_subset.sum(1),axis=0)
normed_subset.plot(kind='barh',stacked=True)
plt.show()
