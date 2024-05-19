import streamlit as st
import pandas as pd
import joblib
import ast
import py7zr
import os

class MovieRecommender:
    def __init__(self):
        self.movies_df = None
        self.genres_list = None
        self.similarity = None

    # Decompress 7z files
    def decompress(self):
        compressed_file = '../models/Models.7z' #dirname + '/models/Models.7z'
        output_dir = '../models' #dirname + '/models'
        try:
            with py7zr.SevenZipFile(compressed_file, mode='r') as z:
                z.extractall(path=output_dir)
        except Exception as e:
            print(e)

    # Read database and get a list of genres
    def GetData(self):
        if self.movies_df is None or self.genres_list is None:
            self.movies_df = pd.read_csv('../data/processed/Movies_Database.csv') #dirname+'/data/processed/Movies_Database.csv'
            self.movies_df['genres'] = self.movies_df['genres'].apply(ast.literal_eval)

            all_genres = set()
            for genres in self.movies_df['genres']:
                all_genres.update(genres)
            self.genres_list = list(all_genres)
            self.genres_list = [e for e in self.genres_list if e != '']

    # Get model from 7z
    def GetModels(self):
        if self.similarity is None:
            if not os.path.exists('../models/cosine_similarity.pkl'): #dirname + '/models/cosine_similarity.pkl'
                self.decompress()
            self.similarity = joblib.load('../models/cosine_similarity.pkl') # dirname + '/models/cosine_similarity.pkl'
       
    # Function to recommend from film name
    def recommend(self, number, movie):
        movie_index = self.movies_df[self.movies_df["original_title"] == movie].index[0]
        distances = self.similarity[movie_index]
        movie_list = sorted(list(enumerate(distances)), reverse = True , key = lambda x: x[1])[1:number]
    
        recommend_films = []
        for i in movie_list:
            recommend_films.append((self.movies_df.iloc[i[0]].original_title))
        return recommend_films

    # Main function
    def main(self):
        self.GetData()

        # Streamlit
        st.title('Movie Recommendation System')

        number = st.slider("Select number of movies to recommend", min_value=1, max_value=10, value=5)
        genre1 = st.selectbox('Select prefered genre:', self.genres_list)
        genre2 = st.selectbox('Select secondary genre:', self.genres_list)

        filtered_movies = self.movies_df[self.movies_df['genres'].apply(lambda x: (genre1 in x) and (genre2 in x))]
        movie_list = filtered_movies['original_title'].tolist()

        # Selector
        selected_movie = st.selectbox("Select a movie", movie_list) if movie_list else None

        if not movie_list:
            st.write("No movies available with the selected genres.")
        elif selected_movie:
            st.write(f"Movies similar to {selected_movie}:")
            if st.button("Recommend similar movies"):
                recommended_movies = self.recommend(number+1, selected_movie)
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





