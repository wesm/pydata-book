import json
from pandas import DataFrame, Series
from matplotlib import pyplot as plt
import pandas as pd;
import numpy as np

path = 'E:\python\pydata-book\ch02\usagov_bitly_data2012-03-16-1331923249.txt'
records = [json.loads(line) for line in open(path)]

frame = DataFrame(records)
# print frame
# print frame['tz'][:10]
tz_counts = frame['tz'].value_counts()
#c_counts = frame['c'].value_counts()
# print tz_counts[:10]
# print c_counts[:10]
# print frame['tz']
clean_tz = frame['tz'].fillna('Missing')
clean_tz[clean_tz == ''] = 'Unknown'
tz_counts = clean_tz.value_counts()
#print tz_counts[:10]
tz_counts[:10].plot(kind='barh',rot=0)
plt.show()