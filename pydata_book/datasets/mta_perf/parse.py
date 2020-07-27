from pandas import DataFrame
from lxml import objectify

path = 'Performance_MNR.xml'
parsed = objectify.parse(open(path))
root = parsed.getroot()

data = []

for elt in root.INDICATOR:
    el_data = {}
    for child in elt.getchildren():
        el_data[child.tag] = child.pyval
    data.append(el_data)

perf = DataFrame(data)
