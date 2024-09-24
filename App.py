import streamlit as st
from PIL import Image
import json
#f rom Recommender import CosineSimilarity,KNearestNeighbours
from Recommenders import CosineSimilarity,KNearestNeighbours
from bs4 import BeautifulSoup
import io
import PIL.Image
from urllib.request import urlopen
from scraper_api import ScraperAPIClient
import re

with open('./Data/movie_data.json', 'r+', encoding='utf-8') as f:
    data = json.load(f) #data holds the one hot encoding+movie rating
with open('./Data/movie_titles.json', 'r+', encoding='utf-8') as f:
    movie_titles = json.load(f) #movie_titles hold the movie name ,movie director,movie actor,index and link in the 2d datastructure
with open('./Data/movie_director.json', 'r+', encoding='utf-8')as f:
    directors = json.load(f)
with open('./Data/movie_actor.json','r+',encoding='utf-8')as f:
    actors=json.load(f)

#movie_titles hold the movie name ,movie director with link and index number in the datastructure

client = ScraperAPIClient("9886a8a83cd7953e83d8566f609ed9faf")
def movie_poster_fetcher(imdb_link):

    url_data = client.get(imdb_link).text
    s_data = BeautifulSoup(url_data, 'html.parser') # Use BeautifulSoup to parse the HTML content
    imdb_dp = s_data.find("meta", property="og:image")    # Find the meta tag that contains the movie poster link
    if imdb_dp is not None:  # If the movie poster link is found, display the poster
        movie_poster_link = imdb_dp.attrs['content']
        u = urlopen(movie_poster_link) # Open the movie poster link and read the raw data
        raw_data = u.read()
        image = PIL.Image.open(io.BytesIO(raw_data))# Use Pillow to open and resize the image
        image = image.resize((158, 301))
        st.image(image, use_column_width=False) # Display the image in the Streamlit app
    else: # If the movie poster link is not found, display an error message
        st.markdown("could not find the link to fetch the movie poster ")

def get_movie_info(imdb_link):
    url_data = client.get(imdb_link).text
    s_data = BeautifulSoup(url_data, 'html.parser')# Use BeautifulSoup to parse the HTML content
    imdb_content = s_data.find("meta", property="og:description")# Find the meta tag that contains the movie description
    if imdb_content is not None: # If the movie description is found, extract the director, cast, and story
        # Extract the movie description and split it by periods
        movie_descr = imdb_content.attrs['content']
        movie_descr = str(movie_descr).split('.')
        # The first sentence contains the director's name
        movie_director = movie_descr[0]
        # The second sentence contains the cast list
        movie_cast = str(movie_descr[1]).replace('With', 'Cast: ').strip()
        # The third sentence contains the movie's story
        movie_story = 'Story: ' + str(movie_descr[2]).strip()+'.'
        # Find the IMDb rating and extract the numerical value(this uses regular expressions)
        rating = s_data.find("span", class_="sc-bde20123-1 iZlgcd")
        number = re.findall(r'\d+\.\d+', str(rating))[0]
        return movie_director,movie_cast,movie_story,number
    else:
        return None,None,None,None

def get_movie_link(title):
    with open('./Data/movie_titles.json', 'r+', encoding='utf-8') as f:
        movie_titles = json.load(f)
    for movie in movie_titles:
        if movie[0] == title:
            return movie[4]


def KNN_Movie_Recommender(test_point, k):

    # Create dummy target variable for the KNN Classifier
    target = [0 for item in movie_titles]
    # Instantiate object for the Classifier
    model = KNearestNeighbours(data, target, test_point, k=k) #instantiating an object
    # Run the algorithm
    model.fit()
    # Print list of 10 recommendations < Change value of k for a different number >
    table = []
    for i in model.indices:
        # Returns back movie title and imdb link
        table.append([movie_titles[i][0], movie_titles[i][4],data[i][-1]])
    print(table)
    return table

st.set_page_config(
   page_title="Movie Recommender System",
)


def main():
    img1 = Image.open("C:/Users/LENOVO/PycharmProjects/MovieRecommender/Meta/Movie_System_Logo.jpg")
    img1 = img1.resize((400,400),)
    st.image(img1,use_column_width=False)
    st.markdown(
        """
        <style>
        body {
            background-color: #FFFF00;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.title("Movie Recommender System")
    st.markdown('''<h4 style='text-align: left; color: #FFFF00;'>* Data is based "IMDB 5000 Movie Dataset"</h4>''',
                unsafe_allow_html=True)
    genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
              'Fantasy', 'Film-Noir', 'Game-Show', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News',
              'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Thriller', 'War', 'Western']
    movies = [title[0] for title in movie_titles]#loops through and appends the first index of the movie_titles 2d list(so the movie name)
    Director = [item[0] for item in directors] #loops through and appends the first index of the directors  2d list(so the director name)
    Actor=[item[0] for item in actors] # #loops through and appends the first index of the actors   2d list(so the actor name)
    unique_Actor=[] #creates a new 1D list which basically removes duplicate names from the actors 2d list by using a for loop + an if condition
    for element in Actor:
        if element not in unique_Actor:
            unique_Actor.append(element)
    unique_Director = []#creates a new 1D list which basically removes duplicate names from the Director 2d list by using a for loop + an if condition
    for element in Director:
        if element not in unique_Director:
            unique_Director.append(element)
    category = ['--Select--', 'Movie based', 'Genre based','Director based','Actor based'] #represents recommendation types as a 1d list
    cat_op = st.selectbox('Select Recommendation Type', category)
    if cat_op == category[0]:  #validation incase the user doesnt input a recommendation type
        st.warning('Please select Recommendation Type!!')
    elif cat_op == category[1]:
        select_movie = st.selectbox('Select movie: (Recommendation will be based on this selection)', ['--Select--'] + movies)
        fetch_poster = st.radio("Want to Fetch Movie Poster?", ('Yes', 'No'))
        st.markdown('''<h4 style='text-align: left; color: #d73b5c;'>* Fetching  Movie Posters will take time."</h4>''',
                    unsafe_allow_html=True)
        if fetch_poster== 'No':
            if select_movie == '--Select--':
                st.warning('Please select Movie!!') #more validation incase user doesnt input a movie
            else:
                no_of_reco = st.slider('Number of movies you want Recommended:', min_value=5, max_value=35, step=1)
                genres = data[movies.index(select_movie)]
                test_points = genres
                table = KNN_Movie_Recommender(test_points, no_of_reco+1)
                table.pop(0)
                c = 0
                st.success('Some of the movies from our Recommendation, have a look below')
                for movie, link, ratings in table:
                    director,cast,story,total_rat = get_movie_info(link)
                    c += 1
                    if director == None:
                        st.markdown("Could not find movie info") #validation incase the html of the movie info dont work
                    else:
                        st.markdown(f"({c})[ {movie}]({link})")
                        st.markdown(director)
                        st.markdown(cast)
                        st.markdown(story)
                        st.markdown('IMDb Rating:'+str(total_rat)+'*')


        else:
            if select_movie == '--Select--':
                st.warning('Please select Movie!!')
            else:
                no_of_reco = st.slider('Number of movies you want Recommended:', min_value=5, max_value=35, step=1)
                genres = data[movies.index(select_movie)]  #takes corresponding movie written as the one hot+imdb rating so eg avatar is index 0 so itll take first index from data list which is a 2d list containgin the one hot encoding + imdb rating
                test_points = genres
                table = KNN_Movie_Recommender(test_points, no_of_reco+1)
                table.pop(0) #removes first movie index from recommendation, thats the movie which will be inputted into search box
                c = 0
                st.success('Some of the movies from our Recommendation, have a look below')
                for movie, link, ratings in table:
                    st.markdown(f"({c})[ {movie}]({link})")
                    c += 1
                    movie_poster_fetcher(link)
                    director,cast,story,total_rat = get_movie_info(link)
                    if director == None:
                        st.markdown("Could not find movie info")
                    else:
                        st.markdown(director)
                        st.markdown(cast)
                        st.markdown(story)
                        st.markdown('IMDb Rating:' + str(total_rat) + '*')

    elif cat_op == category[2]:
        sel_gen = st.multiselect('Select Genres:', genres)
        fetch_poster = st.radio("Want to Fetch Movie Poster?", ('Yes', 'No'))
        st.markdown('''<h4 style='text-align: left; color: #A020F0;'>* Fetching Movie Posters will take time."</h4>''', #disclaimer
                    unsafe_allow_html=True)
        if fetch_poster == 'No':
            if sel_gen:
                imdb_score = st.slider('Choose IMDb score:', 1, 10, 7)
                no_of_reco = st.number_input('Number of movies:', min_value=5, max_value=35, step=1)
                test_point = [1 if genre in sel_gen else 0 for genre in genres]
                test_point.append(imdb_score)
                table = KNN_Movie_Recommender(test_point, no_of_reco)
                c = 0
                st.success('Some of the movies from our Recommendation, have a look below')
                for movie, link, ratings in table:
                    st.markdown(f"({c})[ {movie}]({link})")
                    c += 1
                    director,cast,story,total_rat = get_movie_info(link)
                    if director == None:
                        st.markdown("Could not find movie info")
                    else:
                        st.markdown(director)
                        st.markdown(cast)
                        st.markdown(story)
                        st.markdown('IMDb Rating:' + str(total_rat) + '*')

        else:
            if sel_gen:
                imdb_score = st.slider('Choose IMDb score:', 1, 10, 8)
                no_of_reco = st.number_input('Number of movies:', min_value=5, max_value=35, step=1)
                test_point = [1 if genre in sel_gen else 0 for genre in genres]
                test_point.append(imdb_score)
                table = KNN_Movie_Recommender(test_point, no_of_reco)
                c = 0
                st.success('Some of the movies from our Recommendation, have a look below')
                for movie, link, ratings in table:
                    st.markdown(f"({c})[ {movie}]({link})")
                    movie_poster_fetcher(link)
                    director,cast,story,total_rat = get_movie_info(link)
                    c += 1
                    if director == None:
                        st.markdown("Could not find movie info")
                    else:
                        st.markdown(director)
                        st.markdown(cast)
                        st.markdown(story)
                        st.markdown('IMDb Rating:' + str(total_rat) + '*')

    elif cat_op == category[3]:
        sel_director = st.selectbox('Select Director:', unique_Director)
        fetch_poster = st.radio("Want to Fetch Movie Poster?", ('Yes', 'No'))
        st.markdown('''<h4 style='text-align: left; color: #A020F0;'>* Fetching Movie Posters will take time."</h4>''',
                    unsafe_allow_html=True)
        if fetch_poster== 'No':
            if sel_director == '--Select--':
                st.warning('Please select Director!!')
            else:
                no_of_reco = st.number_input('Number of movies:', min_value=5, max_value=35, step=1)
                object=CosineSimilarity(movie_titles,no_of_reco)
                movie_list=object.recommend_movies_director(sel_director)#recommend_movies_director(sel_director)
                st.success('Some of the movies from our Recommendation, have a look below')
                c=0
                for movie in movie_list:
                    imdblink=get_movie_link(movie)
                    c += 1
                    st.markdown(f"({c})[ {movie}]({imdblink})")
                    director, cast, story, total_rat = get_movie_info(imdblink)
                    if director == None:
                        st.markdown("Could not find movie info")
                    else:
                        st.markdown(director)
                        st.markdown(cast)
                        st.markdown(story)
                        st.markdown('IMDb Rating:' + str(total_rat) + '*')
        else:
            if sel_director == '--Select--':
                st.warning('Please select Movie!!')
            else:
                no_of_reco = st.number_input('Number of movies:', min_value=5, max_value=35, step=1)
                object = CosineSimilarity(movie_titles, no_of_reco)
                movie_list=object.recommend_movies_director(sel_director)#recommend_movies=_director(sel_director)
                st.success('Some of the movies from our Recommendation, have a look below')
                c=0
                for movie in movie_list:
                    imdblink=get_movie_link(movie)
                    movie_poster_fetcher(imdblink)
                    director, cast, story, total_rat = get_movie_info(imdblink)
                    st.markdown(f"({c})[ {movie}]({imdblink})")
                    c+=1
                    if director == None:
                        st.markdown("Could not find movie info")
                    else:
                        st.markdown(director)
                        st.markdown(cast)
                        st.markdown(story)
                        st.markdown('IMDb Rating:' + str(total_rat) + '*')
    elif cat_op == category[4]:
        sel_actor = st.selectbox('Select Actor:', unique_Actor)
        fetch_poster = st.radio("Want to Fetch Movie Poster?", ('Yes', 'No'))
        st.markdown('''<h4 style='text-align: left; color: #A020F0;'>* Fetching Movie Posters will take time.*</h4>''',
                    unsafe_allow_html=True)
        if fetch_poster == 'No':
            if sel_actor == '--Select--':
                st.warning('Please select Movie!!')
            else:
                no_of_reco = st.number_input('Number of movies:', min_value=5, max_value=35, step=1)
                object=CosineSimilarity(movie_titles,no_of_reco)
                st.success('Some of the movies from our Recommendation, have a look below')
                movie_list = object.recommend_movies_actor(sel_actor)
                c=0
                for movie in movie_list:
                    imdblink = get_movie_link(movie)
                    director, cast, story, total_rat = get_movie_info(imdblink)
                    st.markdown(f"({c})[ {movie}]({imdblink})")
                    c+=1
                    if director == None:
                        st.markdown("Could not find movie info")
                    else:
                        st.markdown(director)
                        st.markdown(cast)
                        st.markdown(story)
                        st.markdown('IMDb Rating:' + str(total_rat) + '*')
        else:
            no_of_reco = st.number_input('Number of movies:', min_value=5, max_value=20, step=1)
            object = CosineSimilarity(movie_titles, no_of_reco) #making of object of class Cosine similarity
            movie_list = object.recommend_movies_actor(sel_actor) #calling on the objects method: recommend_movies_actor
            st.success('Some of the movies from our Recommendation, have a look below')
            c=0
            for movie in movie_list:
                imdblink = get_movie_link(movie)
                movie_poster_fetcher(imdblink)
                director, cast, story, total_rat = get_movie_info(imdblink)
                st.markdown(f"({c})[ {movie}]({imdblink})")
                c+=1
                if director==None:
                    st.markdown("Could not find movie info")
                else:
                    st.markdown(director)
                    st.markdown(cast)
                    st.markdown(story)
                    st.markdown('IMDb Rating:' + str(total_rat) + '*')

if __name__ == "__main__":
    main()
