import requests
import streamlit as st
import pickle
import pandas as pd


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=3eaaf306cfc0080522209b730b25dd67'.format(movie_id))
    data = response.json()

    if "poster_path" in data and data["poster_path"] is not None:
        return "https://image.tmdb.org/t/p/original" + data["poster_path"]
    return "https://via.placeholder.com/300"  # Fallback image



def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    movies_list = sorted(list(enumerate(similarity[index])),reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch Poster From API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

similarity = pickle.load(open('similarity.pkl', 'rb'))


movies_list = pickle.load(open('movie_list.pkl', 'rb'))
movies = pd.DataFrame(movies_list)


st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "How would you like to be contacted?",
    movies['title'].values
)

st.write("You selected:", selected_movie_name)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3 , col4 , col5  = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])