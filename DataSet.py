import os
import pandas as pd
import json

# Set working directory
os.chdir('C:/Users/LENOVO/PycharmProjects/MovieRecommender')

# Read in movie metadata CSV file
MovieData = pd.read_csv("C:/Users/LENOVO/PycharmProjects/MovieRecommender/Data/movie_metadata.csv")

# Create a new DataFrame with only relevant columns
df = MovieData[['genres', 'movie_title', 'imdb_score', 'movie_imdb_link', 'director_name', 'actor_1_name']].copy()

# Fill any missing actor and director names with empty strings
df['director_name'] = df['director_name'].fillna('')
df['actor_1_name'] = df['actor_1_name'].fillna('')

# Create a list of all actors in the dataset
actor_all_movies=[]
for i in df.index:
    actor_all_movies.append(df.loc[i]['actor_1_name'])
actor_all_movies.sort()
del actor_all_movies[0:7]
actor=sorted(list(set(actor_all_movies)))

# Create a list of all directors in the dataset
director_all_movies = []
for i in df.index:
    director_all_movies.append((df.loc[i]["director_name"]))
director_all_movies.sort()
del director_all_movies[0:104] #deletes the spaces in the first few indexes
director=sorted(list(set(director_all_movies)))   #director contains unique, alphabeticaly ordered directors

# Create a list of all genres in the dataset
genres_all_movies = [df.loc[i]['genres'].split('|') for i in df.index]
genres = sorted(list(set([item for sublist in genres_all_movies for item in sublist])))

full_data= []  #contains genre one hot encoding+imdb rating
movie_titles = []  #contains movie title, index  number and imdb link ,director name and actor name
director_title=[] #contains director name, index number and imdb link of that specific movie they have directed
actor_title=[] #contains actor name , index number and imdb link of that specific movie they have starred inn
df.to_csv('RequiredAttributes.csv')
for i in df.index:
    # Append movie title, link and the index of the movie
    movie_titles.append((df.loc[i]['movie_title'].strip().strip(),df.loc[i]['director_name'].strip(),df.loc[i]['actor_1_name'], i, df.loc[i]['movie_imdb_link'].strip()))
    #appends director name, link and index of director
    director_title.append((df.loc[i]['director_name'], i, df.loc[i]['movie_imdb_link'].strip()))
    #appends actor name index and imdb link
    actor_title.append((df.loc[i]['actor_1_name'], i, df.loc[i]['movie_imdb_link'].strip()))
    # Add list of genres of the movies (1/0) to movie data
    movie_data = [1 if genre in df.loc[i]['genres'].split('|') else 0 for genre in genres]
    # Add IMDb score of the movie to the movie data
    movie_data.append(df.loc[i]['imdb_score'])
    # Add record of movie to main data list
    full_data.append(movie_data)

# Sort director and actor lists alphabetically and remove empty entries
director_title=sorted(director_title, key=lambda x:x[0],reverse=False)
director_title = [x for x in director_title if x[0] != '']
actor_title = sorted(actor_title, key=lambda x:x[0],reverse=False)
actor_title = [x for x in actor_title if x[0] != '']
data_dump = 'C:/Users/LENOVO/PycharmProjects/MovieRecommender/Data/movie_data.json'
titles_dump = 'C:/Users/LENOVO/PycharmProjects/MovieRecommender/Data/movie_titles.json'
director_dump='C:/Users/LENOVO/PycharmProjects/MovieRecommender/Data/movie_director.json'
actor_dump='C:/Users/LENOVO/PycharmProjects/MovieRecommender/Data/movie_actor.json'

## Open a file at specified location to write movie data in JSON format
# 'w+' flag opens file for reading and writing, and creates the file if it does not exist
# 'encoding' parameter specifies character encoding to be used when writing to the file
with open(data_dump, 'w+', encoding='utf-8') as f:
    # Write the movie data list to the opened file in JSON format
    json.dump(full_data, f)
with open(titles_dump, 'w+', encoding='utf-8') as f:
    json.dump(movie_titles, f)
with open(director_dump,'w',encoding='utf-8')as f:
    json.dump(director_title,f)
with open(actor_dump,'w',encoding='utf-8')as f:
    json.dump(actor_title,f)
