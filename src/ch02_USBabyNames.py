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
