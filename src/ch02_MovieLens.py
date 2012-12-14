#MovieLens 1M Data Set
import pandas as pd
#See http://www.red-dove.com/python_logging.html
import logging
logging.basicConfig()
log = logging.getLogger(None)
log.setLevel(logging.DEBUG) #set verbosity to show all messages of severity >= DEBUG
log.info("Starting ch02_MovieLens!")
#You can verify that everything succeeded by looking at the print result
#users
unames = ['user_id','gender','age','occupation','zip']
users = pd.read_table('../ch02/movielens/users.dat',sep='::',header=None,names=unames)
#print(users[:5])
logging.info("users:")
logging.info(users[:5])
#ratings
rnames = ['user_id','movie_id','rating','timestamp']
ratings = pd.read_table('../ch02/movielens/ratings.dat',sep='::',header=None,names=rnames)
#print(ratings[:5])
logging.info("ratings:")
logging.info(ratings[:5])
#movies
mnames = ['movie_id','title','genres']
movies = pd.read_table('../ch02/movielens/movies.dat',sep='::',header=None,names=mnames)
#print(movies[:5])
logging.info("movies:")
logging.info(movies[:5])
#we first merge ratings with users then merging that result with the movies data. 
#pandas infers which columns to use as the merge (or join) keys based on overlapping names:
data = pd.merge(pd.merge(ratings,users),movies)
#print(data)
logging.info("merged data:")
logging.info(data)
#data_index
logging.info("merged data index[0]:")
logging.info(data.ix[0])
#data_mean_rating
mean_rating = data.pivot_table('rating', rows='title', cols='gender',aggfunc='mean')
logging.info("merged data mean rating[:5]:")
logging.info(mean_rating[:5])
#group the data by title and use size() to get a Series of group sizes for each title:
rating_by_title = data.groupby('title').size()
logging.info("merged data rating_by_title:")
logging.info(rating_by_title)
#active_titles >250
active_titles = rating_by_title.index[rating_by_title >= 250]
logging.info("merged data active_titles:")
logging.info(active_titles)
#mean_ratings of active_titles >250
mean_ratings = mean_rating.ix[active_titles]
logging.info("merged data mean_ratings of active_titles>250:")
logging.info(mean_ratings)
#top_female_ratings
top_female_ratings = mean_ratings = mean_ratings.sort_index(by='F',ascending=False)
logging.info("merged data top_female_ratings(10) of mean_ratings:")
logging.info(top_female_ratings[:10])
#Measuring rating disagreement
mean_ratings['diff'] = mean_ratings['M'] - mean_ratings['F']
sort_by_diff = mean_ratings.sort_index(by='diff')
logging.info("merged data mean_ratings of mean_ratings:")
logging.info(sort_by_diff[:15])
# Reverse order of rows, take first 15 rows
# We get the movies preferred by man that women didnot rate as highly:
logging.info(sort_by_diff[::-1][:15])
# Standard deviation of rating grouped by title
rating_std_by_title = data.groupby('title')['rating'].std()
# Filter down to active_titles
rating_std_by_title = rating_std_by_title.ix[active_titles]
# Order Series by value in descending order
order_series = rating_std_by_title.order(ascending=False)[:10]
logging.info("merged data order_series of mean_ratings:")
logging.info(order_series)
log.info("End of ch02_MovieLens!")