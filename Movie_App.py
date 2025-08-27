import streamlit as st
import pickle
import pandas as pd
import requests
    
st.title("Movie Recommendation App")
st.write("Welcome to the Movie Recommendation App!")
st.write("Here you can find movie recommendations based on your preferences.")
st.write("Enjoy exploring new movies!")

# Load data
movies_dict = pickle.load(open('movies_dict.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
movies = pd.DataFrame(movies_dict)

# Dropdown for movie selection
selected_movie = st.selectbox(
    "Select a movie from the dropdown below to get recommendations.",
    movies['title'].values
)

# Function to fetch poster from TMDB API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=a139f8585b021104d7c75c3e0f55d603"
    response = requests.get(url).json()
    poster_path = response.get('poster_path', None)
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        # Fallback if poster not found
        return "https://via.placeholder.com/500x750?text=No+Image"

# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    # sort movies by similarity score, skipping the first (itself)
    movie_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]
    
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
        
    return recommended_movie_names, recommended_movie_posters

# UI
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    cols = st.columns(5)  # Create 5 columns
    for i, col in enumerate(cols):
        with col:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])
