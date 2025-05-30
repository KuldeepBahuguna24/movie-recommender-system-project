import streamlit as st
import pickle
import pandas as pd
import requests

# to fetch the movies poster
def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]  # this line will find the movie index

    distances = similarity[movie_index]  # distance between all movies

    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    # enumerate function will change list into tupple  and sort it then reverse it and return 1 to 6 similar movies..

    recommended_movies = []
    recommended_movies_poster=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_poster


movies_dict=pickle.load(open('movie_dict.pkl', 'rb'))
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name=st.selectbox(
'How would you like to be connected ?',
movies['title'].values)

if st.button('Recommend'):
   names,poster=recommend(selected_movie_name)

   col1,col2,col3,col4,col5=st.columns(5)
   with col1:
       st.text(names[0])
       st.image(poster[0])
   with col2:
       st.text(names[1])
       st.image(poster[1])
   with col3:
       st.text(names[2])
       st.image(poster[2])
   with col4:
       st.text(names[3])
       st.image(poster[3])
   with col5:
       st.text(names[4])
       st.image(poster[4])