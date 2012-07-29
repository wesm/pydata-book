from pandas import *
from pandas.util.decorators import cache_readonly
import numpy as np
import os

base = 'ml-100k'

class IndexedFrame(object):
    """

    """

    def __init__(self, frame, field):
        self.frame = frame

    def _build_index(self):
        pass

class Movielens(object):

    def __init__(self, base='ml-100k'):
        self.base = base

    @cache_readonly
    def data(self):
        names = ['user_id', 'item_id', 'rating', 'timestamp']
        path = os.path.join(self.base, 'u.data')
        return read_table(path, header=None, names=names)

    @cache_readonly
    def users(self):
        names = ['user_id', 'age', 'gender', 'occupation', 'zip']
        path = os.path.join(self.base, 'u.user')
        return read_table(path, sep='|', header=None, names=names)

    @cache_readonly
    def items(self):
        names = ['item_id', 'title', 'release_date', 'video_date',
                 'url', 'unknown', 'Action', 'Adventure', 'Animation',
                 "Children's", 'Comedy', 'Crime', 'Documentary', 'Drama',
                 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery',
                 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
        path = os.path.join(self.base, 'u.item')
        return read_table(path, sep='|', header=None, names=names)

    @cache_readonly
    def genres(self):
        names = ['name', 'id']
        path = os.path.join(self.base, 'u.genre')
        data = read_table(path, sep='|', header=None, names=names)[:-1]
        return Series(data.name, data.id)

    @cache_readonly
    def joined(self):
        merged = merge(self.data, self.users)
        merged = merge(merged, self.items)
        return merged

    def movie_stats(self, title):
        data = self.joined[self.joined.title == title]

        return data.groupby('gender').rating.mean()

def biggest_gender_discrep(data):
    nobs = data.pivot_table('rating', rows='title',
                            cols='gender', aggfunc=len, fill_value=0)
    mask = (nobs.values > 10).all(1)
    titles = nobs.index[mask]

    mean_ratings = data.pivot_table('rating', rows='title',
                                    cols='gender', aggfunc='mean')
    mean_ratings = mean_ratings.ix[titles]

    diff = mean_ratings.M - mean_ratings.F
    return diff[np.abs(diff).argsort()[::-1]]

buckets = [0, 18, 25, 35, 50, 80]

ml = Movielens()
title = 'Cable Guy, The (1996)'
