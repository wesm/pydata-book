#US Baby Names 1880-2010
#The United States Social Security Administration (SSA) has made available data 
#on the frequency of baby names from 1880 through the present.
import pandas as pd
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