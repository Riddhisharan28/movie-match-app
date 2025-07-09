import streamlit as st
import pickle
import pandas as pd
import requests
import time

# --- Function to fetch poster image from TMDB API ---
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=e0df18ca2600c6b86b27a3d89c077c45&language=en-US"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return "https://image.tmdb.org/t/p/w500" + data['poster_path']
    except Exception as e:
        print("Error fetching poster:", e)
        return "https://via.placeholder.com/500x750?text=No+Poster"

# --- Recommendation function ---
def recommend(movie):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
    except IndexError:
        st.error("❌ Movie not found in the database. Please check the name.")
        return [], []

    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        poster_url = fetch_poster(movie_id)
        recommended_movies_posters.append(poster_url)
        time.sleep(0.25)  # Rate-limit friendly

    return recommended_movies, recommended_movies_posters

# --- Load data and similarity matrix ---
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# --- Streamlit UI ---
st.title('Movie Match 🎬')

selected_movie_name = st.selectbox(
    'Search and Select a Movie:',
    movies['title'].values
)

if st.button('Recommend Movies'):
    names, posters = recommend(selected_movie_name)
    if names:
        cols = st.columns(5)
        for idx, col in enumerate(cols):
            with col:
                st.text(names[idx])
                st.image(posters[idx])
                
