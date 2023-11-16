
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import re
import sys
import itertools
import json


# from sklearn.metrics.pairwise import cosine_similarity
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.manifold import TSNE
 
import warnings
warnings.filterwarnings('ignore')

###
# Reading in data
###
tracks = pd.read_csv('tracks.csv')
# print(tracks.head())

artists = pd.read_csv('artists.csv')
# print(artists.head())

###
# Updating genre to list
###
artists['genres_upd'] = artists['genres'].apply(lambda x: [re.sub(' ','_',i) for i in re.findall(r"'([^']*)'", x)])

artists['genres_upd'].values[9434][0]

###
# Updating artist to list
###
tracks['artists_upd_v1'] = tracks['artists'].apply(lambda x: re.findall(r"'([^']*)'", x))
tracks['artists_upd_v2'] = tracks['artists'].apply(lambda x: re.findall('\"(.*?)\"',x))
tracks['artists_upd'] = np.where(tracks['artists_upd_v1'].apply(lambda x: not x), tracks['artists_upd_v2'], tracks['artists_upd_v1'] )

###
# Removing song duplicates
###
tracks['artists_song'] = tracks.apply(lambda row: row['artists_upd'][0]+str(row['name']),axis = 1)
tracks.sort_values(['artists_song','release_date'], ascending = False, inplace = True)
# print(tracks[tracks['name']=='Lover'])

tracks.drop_duplicates('artists_song',inplace = True)
# print(tracks[tracks['name']=='Lover'])


###
# Explode songs with multiple artists
###

# print(tracks[tracks['name']=='Under Pressure'])
tracks = tracks.explode('artists_upd')

# print(tracks[tracks['name']=='Under Pressure'])

artists_exploded = tracks.merge(artists, how = 'left', left_on = 'artists_upd',right_on = 'name')
artists_exploded = artists_exploded[~artists_exploded.genres_upd.isnull()]

# print(artists_exploded_enriched[artists_exploded['id_x'] =='5oidljiMjeJTWUGZ4TfFea'])


###
# Merge genre list
###
artists_genres = artists_exploded.groupby('id_x')['genres_upd'].apply(list).reset_index()
artists_genres['genre_list'] = artists_genres['genres_upd'].apply(lambda x: list(set(list(itertools.chain.from_iterable(x)))))
# print(artists_genres.head())

tracks = tracks.merge(artists_genres[['id_x','genre_list']], how = 'left', left_on = 'id', right_on='id_x')


###
# Drop any rows where the genre is null
###

# print(tracks[tracks['artists_upd']=='Taylor Swift'])
# print(tracks.info())
# print(tracks.isnull().sum())
tracks.dropna(subset=['genre_list'], inplace=True)

print(tracks.isnull().sum())

