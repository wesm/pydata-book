#US Baby Names 1880-2010
#The United States Social Security Administration (SSA) has made available data 
#on the frequency of baby names from 1880 through the present.
import pandas as pd
import numpy as np
#See http://www.red-dove.com/python_logging.html
import logging
logging.basicConfig()
log = logging.getLogger(None)
log.setLevel(logging.DEBUG) #set verbosity to show all messages of severity >= DEBUG
log.info("Starting ch03_USBabyNames!")
#import matplotlib.pyplot as plot
#plot(np.arange(10))
#Load into DataFrame
names1880 = pd.read_csv('../ch02/names/yob1889.txt',names=['name','sex','births'])
logging.info("names1880 raw data:")
logging.info(names1880)
#For the simplicity's sake,total_number_of_births
total_number_of_births = names1880.groupby('sex').births.sum()
logging.info("total_number_of_births:")
logging.info(total_number_of_births)
#assemble all of the data into a single DataFrame and further to add a year field.
# 2010 is the last available year right now
years = range(1889,2011)
pieces = []
columns = ['name','sex','births']

for year in years:
    path = '../ch02/names/yob%d.txt' % year
    frame = pd.read_csv(path,names=columns)
    
    frame['year'] = year
    pieces.append(frame)
    # Concatenate everything into a single DataFrame
    names = pd.concat(pieces,ignore_index=True)
#Logging
logging.info('names in DataFrame:')
logging.info(names)
#Start aggregating the data at the year and sex level using groupby or pivot_table
total_births = names.pivot_table('births',rows='year',cols='sex',aggfunc=sum)
#Logging
logging.info('total_births.tail():')
logging.info(total_births.tail())
#Plot
total_births.plot(title='Total births by sex and year')
#we group the data by year and sex, then add the new column to each group:
def add_prop(group):
    #Insert division floors
    births = group.births.astype(float)
    
    group['prop'] = births/births.sum()
    return group
#
names = names.groupby(['year','sex']).apply(add_prop)
#Logging
logging.info('names.groupby:')
logging.info(names)
#Sanity check
sCheck = np.allclose(names.groupby(['year','sex']).prop.sum(),1)
logging.info('sanity check:')
logging.info(sCheck)
#The top 1000 names
def get_top1000(group):
    return group.sort_index(by='births',ascending=False)[:1000]
grouped = names.groupby(['year','sex'])
top1000 = grouped.apply(get_top1000)
logging.info('Top1000 names:')
logging.info(top1000)
#do-it-yourself
pieces = []
for year, group in names.groupby(['year', 'sex']):
    pieces.append(group.sort_index(by='births', ascending=False)[:1000])
top1000 = pd.concat(pieces, ignore_index=True)
logging.info('Top1000 names(DIY):')
logging.info(top1000)
#Analyzing naming trends
boys = top1000[top1000.sex == 'M']
girls = top1000[top1000.sex == 'F']
total_births = top1000.pivot_table('births',rows='year',cols='name',aggfunc=sum)
#Handlful names using DataFrame's plot
logging.info('Name trends:')
logging.info(total_births)
#Subset
subset = total_births[['John','Harry','Mary','Marilyn']]
logging.info('Name trends subset:')
logging.info(subset)
#Measuring the increase in naming diversity
#Plot
#subset.plot(subplots=True,figsize=(12,10),grid=False,title='Number of births per year')
#Boy names from 2010:
df = boys[boys.year == 2000]
logging.info('Boy names from 2010:')
logging.info(df)
#How many of the most popular names it takes to reach 50%
prop_cumsum = df.sort_index(by='prop',ascending=False).prop.cumsum()
logging.info('How many of the most popular names it takes to reach 50%:')
logging.info(prop_cumsum[:10])
#Search sorted
logging.info(prop_cumsum.searchsorted(0.5))
#In 1900
df = boys[boys.year == 1990 ]
in1990 = df.sort_index(by='prop',ascending=False).prop.cumsum()
in1990_searchsorted = in1990.searchsorted(0.5)+1
logging.info("in 1900 this number was much smaller:")
logging.info(in1990_searchsorted)
#the count for each group
def get_quantile_count(group,q=0.5):
    group = group.sort_index(by='prop',ascending=False)
    return group.prop.cumsum().searchsorted(q)+1
diversity = top1000.groupby(['year','sex']).apply(get_quantile_count)
diversity = diversity.unstack('sex')
logging.info("quantile count:")
logging.info(diversity.head())
#diversity.plot(title="Number of popular names in top 50%")
#The "Last letter " revolution
# extract last letter from name column
get_last_letter = lambda x:x[-1]
last_letters = names.name.map(get_last_letter)
last_letters.name = 'last_letter'
table = names.pivot_table('births',rows=last_letters,cols=['sex','year'],aggfunc=sum)
#select out three representative years spanning the history and print the first few rows:
subtable = table.reindex(columns=[1910,1960,2010],level='year')
logging.info("select out three representative years spanning the history and print the first few rows:")
logging.info(subtable.head())
#a new table containing proportion of total births for each sex ending in each letter:
logging.info("a new table containing proportion of total births for each sex ending in each letter:")
logging.info(subtable.sum())
#letter prop
letter_prop = subtable / subtable.sum().astype(float)
logging.info("letter prop:")
logging.info(letter_prop)
#Plot letter prop
#import matplotlib.pyplot as plt
#fig, axes = plt.subplots(2, 1, figsize=(10, 8))
#letter_prop['M'].plot(kind='bar', rot=0, ax=axes[0], title='Male')
#letter_prop['F'].plot(kind='bar', rot=0, ax=axes[1], title='Female',legend=False)
#transposing to make each column a time series:
letter_prop = table/table.sum().astype(float)
dny_ts = letter_prop.ix[['d','n','y'],'M'].T
logging.info("transposing to make each column a time series:")
logging.info(dny_ts.head())
#a plot of the trends over time again with its plot method
#dny_ts.plot()
#Boy names that became girl names (and vice versa)
all_names = top1000.name.unique()
mask = np.array(['lesl' in x.lower() for x in all_names])
lesley_like = all_names[mask]
logging.info("lesley_like in all names:")
logging.info(lesley_like)
#filter down to just those names and sum births grouped by name
#to see the relative frequencies:
filtered = top1000[top1000.name.isin(lesley_like)]
filteredResult = filtered.groupby('name').births.sum()
logging.info('filter down the lesley like names:')
logging.info(filteredResult)
#aggregate by sex and year and normalize within year:
table = filtered.pivot_table('births',rows='year',cols='sex',aggfunc='sum')
table = table.div(table.sum(1),axis=0)
logging.info("aggregate by sex and year and normalize within year:")
logging.info(table.tail())
#Lastly,it's now easy to make a plot of the breakdown by sex over time
#table.plot(style={'M': 'k-', 'F': 'k--'})
#Conclusions and The Path Ahead