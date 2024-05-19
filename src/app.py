import streamlit as st
import pandas as pd
import joblib
import ast
import py7zr
import os
import pathlib

def decompress(dirname):
    compressed_file = os.path.join(dirname, 'models', 'Models.7z')
    output_dir = os.path.join(dirname, 'models')
    try:
        with py7zr.SevenZipFile(compressed_file, mode='r') as z:
            z.extractall(path=output_dir)
    except Exception as e:
        st.error(f"Error decompressing file: {e}")

def load_data(dirname):
    try:
        movies_df = pd.read_csv(os.path.join(dirname, 'data', 'processed', 'Movies_Database.csv'))
        movies_df['genres'] = movies_df['genres'].apply(ast.literal_eval)

        all_genres = set()
        for genres in movies_df['genres']:
            all_genres.update(genres)
        genres_list = [e for e in list(all_genres) if e != '']

        return movies_df, genres_list
    except Exception as e:
        st.error(f"Error reading data: {e}")
        return None, []

def load_model(dirname):
    try:
        model_path = os.path.join(dirname, 'models', 'cosine_similarity.pkl')
        if not os.path.exists(model_path):
            decompress(dirname)
        similarity = joblib.load(model_path)
        return similarity
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

class MovieRecommender:
    def __init__(self):
        self.dirname = str(pathlib.Path(__file__).parent.parent)
        self.movies_df, self.genres_list = load_data(self.dirname)
        self.similarity = load_model(self.dirname)

    def recommend(self, number, movie):
        if self.similarity is None:
            st.error("Model not loaded. Please try again later.")
            return []

        try:
            movie_index = self.movies_df[self.movies_df["original_title"] == movie].index[0]
        except IndexError:
            st.error("Movie not found in the database.")
            return []

        distances = self.similarity[movie_index]
        movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:number]

        recommend_films = []
        for i in movie_list:
            recommend_films.append(self.movies_df.iloc[i[0]].original_title)
        return recommend_films

    def main(self):
        if self.movies_df is None or not self.genres_list:
            st.error("Error loading data. Please try again later.")
            return

        st.title('Movie Recommendation System')

        number = st.slider("Select number of movies to recommend", min_value=1, max_value=10, value=5)
        genre1 = st.selectbox('Select preferred genre:', self.genres_list)
        genre2 = st.selectbox('Select secondary genre:', [g for g in self.genres_list if g != genre1])

        filtered_movies = self.movies_df[self.movies_df['genres'].apply(lambda x: (genre1 in x) and (genre2 in x))]
        movie_list = filtered_movies['original_title'].tolist()

        selected_movie = st.selectbox("Select a movie", movie_list) if movie_list else None

        if not movie_list:
            st.write("No movies available with the selected genres.")
        elif selected_movie:
            st.write(f"Movies similar to {selected_movie}:")
            if st.button("Recommend similar movies"):
                recommended_movies = self.recommend(number + 1, selected_movie)
                if recommended_movies:
                    for movie in recommended_movies:
                        st.write(movie)
                else:
                    st.write("No similar movies found.")
        else:
            st.warning("Please select a movie to recommend.")

if __name__ == '__main__':
    recommender = MovieRecommender()
    recommender.main()






