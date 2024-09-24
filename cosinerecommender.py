import json
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def recommend_movies_director(director,no_of_reco,data): #data being the link
    #with open('./Data/movie_titles.json', 'r+', encoding='utf-8') as f:
     #   data = json.load(f)
    movies_df = pd.DataFrame(data, columns=['title','actor', 'director', 'index', 'imdb_link'])
    director_matrix = pd.get_dummies(movies_df['director'])
    director_similarity = cosine_similarity(director_matrix)
    director_indices = movies_df[movies_df['director'] == director].index
    if len(director_indices) == 0:
        print("No movies found for the given director")
        return []
    director_index = director_indices[0]
    similarity_scores = list(enumerate(director_similarity[director_index]))
    sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    top_movies = [movies_df.iloc[i]['title'] for i, score in sorted_scores[1:no_of_reco+1]]
    return top_movies


def recommend_movies_actor(actor,no_of_reco,data):
    #with open('./Data/movie_titles.json', 'r+', encoding='utf-8') as f:
        #data = json.load(f)
    movies_df = pd.DataFrame(data, columns=['title', 'director','actor', 'index', 'imdb_link'])
    actor_matrix = pd.get_dummies(movies_df['actor'])
    actor_similarity = cosine_similarity(actor_matrix)
    actor_indices = movies_df[movies_df['actor'] == actor].index
    if len(actor_indices) == 0:
        print("No movies found for the given director")
        return []
    director_index = actor_indices[0]
    similarity_scores = list(enumerate(actor_similarity[director_index]))
    sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    top_movies = [movies_df.iloc[i]['title'] for i, score in sorted_scores[1:no_of_reco + 1]]
    return top_movies