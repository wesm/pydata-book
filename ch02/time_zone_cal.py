# -*- coding:utf-8 -*-

import json
from collections import defaultdict
from collections import Counter


def get_counts(sequence):
    counts = {}
    for x in sequence:
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1
    return counts


def get_counts2(sequence):
    counts = defaultdict(int)
    for x in sequence:
        counts[x] += 1
    return counts


def top_counts(count_dict, n=10):
    # 原来dict的('Europe/Lisbon', 8)调换k、v的位置变成(8,'Europe/Lisbon')，用于后一步的排序
    value_key_pairs = [(count, tz) for tz, count in count_dict.items()]
    # print value_key_pairs
    # value_key_pairs.sort(reverse = True)
    # return value_key_pairs[:n]
    value_key_pairs.sort()
    return value_key_pairs[-n:]


path = 'E:\python\pydata-book\ch02\usagov_bitly_data2012-03-16-1331923249.txt'
records = [json.loads(line) for line in open(path)]
# print records[0]['tz']

time_zone_list = [rec['tz'] for rec in records if 'tz' in rec]
# print time_zone_list[:10]
# print len(time_zone_list)
counts = get_counts(time_zone_list)
# counts2 = get_counts2(time_zone_list)
# print counts['America/New_York']
# print counts
# print counts2
# print top_counts(counts)

counts = Counter(time_zone_list)
print counts.most_common(10)
