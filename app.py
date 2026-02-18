import os
import pickle
import streamlit as st
import pandas as pd
import requests
import gdown


similarity_file_id = "1y-CwNmDp9vuBjB9CHYXtJJrbhI_uiI-v"
similarity_url = f"https://drive.google.com/uc?id={similarity_file_id}"

if not os.path.exists("similarity.pkl"):
    print("Downloading similarity.pkl...")
    gdown.download(similarity_url, "similarity.pkl", quiet=False)



credits_file_id = "1XW_nrJyfS00y-MeedeQkxbJsA4EF8isb"
credits_url = f"https://drive.google.com/uc?id={credits_file_id}"

if not os.path.exists("tmdb_5000_credits.csv"):
    print("Downloading credits file...")
    gdown.download(credits_url, "tmdb_5000_credits.csv", quiet=False)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

movies_path = os.path.join(BASE_DIR, "movies_dict.pkl")
similarity_path = os.path.join(BASE_DIR, "similarity.pkl")

movies_dict = pickle.load(open(movies_path, "rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open(similarity_path, "rb"))





def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=14cd430f1b5a402ccf71667acb72c12f"
        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get("poster_path"):
            return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
        else:
            return None

    except Exception as e:
        print("Error fetching poster:", e)
        return None




def recommended(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]]["movie_id"]

        recommended_movies.append(movies.iloc[i[0]]["title"])
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters




st.title("🎬 Movie Recommendation System")

selected_movie_name = st.selectbox(
    "Select a movie",
    movies["title"].values
)

if st.button("Recommend"):

    names, posters = recommended(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    columns = [col1, col2, col3, col4, col5]

    for i in range(5):
        with columns[i]:
            st.text(names[i])
            if posters[i]:
                st.image(posters[i])
            else:
                st.write("Poster not available")
