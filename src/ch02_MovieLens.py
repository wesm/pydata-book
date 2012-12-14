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
