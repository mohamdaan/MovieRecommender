import numpy as np
from operator import itemgetter
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import streamlit as st
import json
with open('./Data/movie_titles.json', 'r+', encoding='utf-8') as f:
    movie_titles = json.load(f)

class KNearestNeighbours:
   def __init__(self, data, target, test_point, k):
       self.data = data
       self.target = target
       self.test_point = test_point
       self.k = k
       self.distances = list()
       self.categories = list()
       self.indices = list()
       self.counts = list()
       self.category_assigned = None

   @staticmethod
   def dist(p1, p2):
       """Method returns the euclidean distance between two points"""
       return np.linalg.norm(np.array(p1) - np.array(p2))

   def fit(self):
       """Method that performs the KNN classification"""
       # Create a list of (distance, index) tuples from the test point to each point in the data
       self.distances.extend([(self.dist(self.test_point, point), i) for point, i in zip(self.data, [i for i in range(len(self.data))])])
       # Sort the distances in ascending order
       sorted_li = sorted(self.distances, key=itemgetter(0))
       # Fetch the indices of the k nearest point from the data
       self.indices.extend([index for (val, index) in sorted_li[:self.k]])
       # Fetch the categories from the train data target
       for i in self.indices:
           self.categories.append(self.target[i])
       # Fetch the count for each category from the K nearest neighbours
       self.counts.extend([(i, self.categories.count(i)) for i in set(self.categories)])
       # Find the highest repeated category among the K nearest neighbours
       self.category_assigned = sorted(self.counts, key=itemgetter(1), reverse=True)[0][0]

class CosineSimilarity:
   def __init__(self, data,no_of_reco):
       self.data=data
       self.no_of_reco=no_of_reco

   def recommend_movies_director(self,director):  # data being the link
       # with open('./Data/movie_titles.json', 'r+', encoding='utf-8') as f:
       #data = json.load(f)
       movies_df = pd.DataFrame(self.data, columns=['title',  'director','actor', 'index', 'imdb_link'])
       director_matrix = pd.get_dummies(movies_df['director'])
       director_similarity = cosine_similarity(director_matrix)
       director_indices = movies_df[movies_df['director'] == director].index
       if len(director_indices) == 0:
           st.markdown("No movies found for the given director")
           return []
       director_index = director_indices[0]
       similarity_scores = list(enumerate(director_similarity[director_index]))
       sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
       top_movies = [movies_df.iloc[i]['title'] for i, score in sorted_scores[1:self.no_of_reco + 1]]
       return top_movies

   def recommend_movies_actor(self,actor):
       # with open('./Data/movie_titles.json', 'r+', encoding='utf-8') as f:
       # data = json.load(f)
       movies_df = pd.DataFrame(self.data, columns=['title', 'director', 'actor', 'index', 'imdb_link'])
       actor_matrix = pd.get_dummies(movies_df['actor'])
       actor_similarity = cosine_similarity(actor_matrix)
       actor_indices = movies_df[movies_df['actor'] == actor].index
       if len(actor_indices) == 0:
           st.markdown("No movies found for the given director")
           return []
       actor_index = actor_indices[0]
       similarity_scores = list(enumerate(actor_similarity[actor_index]))
       sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
       top_movies = [movies_df.iloc[i]['title'] for i, score in sorted_scores[1:self.no_of_reco + 1]]
       return top_movies

object = CosineSimilarity(movie_titles, 9)
print(object.recommend_movies_director("Quentin Tarantino"))