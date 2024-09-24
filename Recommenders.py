import json
import pandas as pd
import numpy as np
from operator import itemgetter
import streamlit as st

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

    def __init__(self, data, no_of_reco):
        self.data = data #this is the movie titles json file , it holds the movie title, director name , actor name, index and imdb link
        self.no_of_reco = no_of_reco #the number of recommendations inputted by the user

    def cosine_similarity_matrix(self, matrix):
        dot_product = np.dot(matrix, matrix.T)#Calculate the dot product of the input matrix with its transpose to get the dot product matrix
        row_norms = np.sqrt(np.sum(np.square(matrix), axis=1, keepdims=True))# Calculate the row-wise norms of the matrix
        outer_product = np.dot(row_norms, row_norms.T)# Calculate the outer product of the row norms
        cosine_similarities = dot_product / outer_product# Calculate the cosine similarities between each row of the matrix
        return cosine_similarities

    def recommend_movies_director(self, director):
        movies_df = pd.DataFrame(self.data, columns=['movie_title', 'director_name', 'actor_1_name', 'index', 'imdb_link'])# Convert the data into a DataFrame with specific columns
        director_indices = movies_df[movies_df['director_name'] == director].index.tolist()# Get the indices of the rows in the DataFrame where the actor's name matches the given actor name
        if len(director_indices) == 0:
            st.markdown("No movies found for the given director")
            return []
        director_matrix = pd.get_dummies(movies_df['director_name'])# create a matrix where each column represents a director and each row represents a movie
                                                                    # the matrix is one-hot encoded based on the directors of each movie
        director_similarity = self.cosine_similarity_matrix(director_matrix.values)# calculate the cosine similarity matrix for the director matrix
        # get the index of the director and create a list of similarity scores with other directors
        director_index = director_indices[0]
        similarity_scores = list(enumerate(director_similarity[director_index]))
        # sort the similarity scores and extract the top recommendations
        sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        top_movies = [movies_df.iloc[i]['movie_title'] for i, score in sorted_scores[1:self.no_of_reco + 1]]
        return top_movies

    def recommend_movies_actor(self, actor):
        movies_df = pd.DataFrame(self.data, columns=['movie_title', 'director_name', 'actor_1_name', 'index', 'imdb_link'])# Convert the data into a DataFrame with specific columns
        director_indices = movies_df[movies_df['actor_1_name'] == actor].index.tolist()# Get the indices of the rows in the DataFrame where the actor's name matches the given actor name
        if len(director_indices) == 0:# check if any movies are found for the given actor, otherwise return an empty list
            st.markdown("No movies found for the given director")
            return []
        actor_matrix = pd.get_dummies(movies_df['actor_1_name'])# create a matrix where each column represents an actor and each row represents a movie
                                                                # the matrix is one-hot encoded based on the actors of each movie
        actor_similarity = self.cosine_similarity_matrix(actor_matrix.values)# calculate the cosine similarity matrix for the actor matrix
        # get the index of the actor and create a list of similarity scores with other actors
        actor_index = director_indices[0]
        similarity_scores = list(enumerate(actor_similarity[actor_index]))
        # sort the similarity scores and extract the top recommendations
        sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        top_movies = [movies_df.iloc[i]['movie_title'] for i, score in sorted_scores[1:self.no_of_reco + 1]]
        return top_movies

object = CosineSimilarity(movie_titles, 8)
print(object.recommend_movies_actor("Quentin Tarantino"))
