#!/usr/bin/env python
# coding: utf-8
import nltk
import numpy as np
import pandas as pd
import ast
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
import requests
warnings.filterwarnings("ignore", category=DeprecationWarning)
pd.set_option('mode.chained_assignment', None)

movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')

movies = movies.merge(credits,on='title')

movies = movies[['id','title','overview','genres','keywords','cast','crew']]

movies.dropna(inplace=True)

def convert(obj):
    l=[]
    for i in ast.literal_eval(obj):
        l.append(i['name'])
    return l

movies['genres'] = movies['genres'].apply(convert)

movies['keywords'] = movies['keywords'].apply(convert)

def cast_fetch(obj):
    l=[]
    c=0
    for i in ast.literal_eval(obj):
        if c!=3:
            l.append(i['name'])
            c+=1
        else:
            break
    return l

movies['cast']=movies['cast'].apply(cast_fetch)

def fetch_director(obj):
    l=[]
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            l.append(i['name'])
    return l

movies['crew'] = movies['crew'].apply(fetch_director)

movies['overview'] = movies['overview'].apply(lambda x:x.split())

movies['genres'] = movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast'] = movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew'] = movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])

movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

movie = movies[['id','title','tags']]

movie['tags'] = movie['tags'].apply(lambda x:" ".join(x))

ps = PorterStemmer()

def stem(text):
    y=[]
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

movie['tags'] = movie['tags'].apply(stem)

movie['tags'] = movie['tags'].apply(lambda x:x.lower())

cv = CountVectorizer(max_features=5000,stop_words='english')

vectors = cv.fit_transform(movie['tags']).toarray()

similarity = cosine_similarity(vectors)

def recommend(movie_name):
    Result=[]
    Result_id=[]
    movie_index = movie[movie['title']== movie_name].index[0]
    distances =similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    
    for i in movies_list:
        Result.append(movie.iloc[i[0]].title)
        Result_id.append(movie.iloc[i[0]].id)

    return Result,Result_id

def get_suggestions():
    return list(movie['title'].str.capitalize())

def fetch_poster(movie_id):
    response = requests.get('')




