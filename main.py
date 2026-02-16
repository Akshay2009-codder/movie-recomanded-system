import numpy as np
import pandas as pd

movies = pd.read_csv("tmdb_5000_movies.csv")
credit = pd.read_csv("tmdb_5000_credits.csv")

movies = movies.merge(credit, on='title')
movies = movies[["movie_id","genres","homepage","keywords","overview","cast","crew"]]
print(movies.head())