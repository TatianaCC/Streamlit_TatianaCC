import streamlit as st
import pandas as pd
import joblib
import ast
import pathlib

dirname = str(pathlib.Path(__file__).parent.parent)

# Read database
movies_df = pd.read_csv(dirname+'/data/processed/Movies_Database.csv')
movies_df['genres'] = movies_df['genres'].apply(ast.literal_eval)

all_genres = set()
for genres in movies_df['genres']:
    all_genres.update(genres)
genres_list = list(all_genres)
genres_list = [e for e in genres_list if e != '']
director = movies_df['director'].unique()


# Load models


# Function fo recommend from film name
def recommend(number, movie):
    movie_index = movies_df[movies_df["original_title"] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse = True , key = lambda x: x[1])[1:number]
  
    recommend_films = []
    for i in movie_list:
        recommend_films.append((movies_df.iloc[i[0]].original_title))
    return recommend_films

def filter():
    filtered_movies = movies_df[movies_df['genres'].apply(lambda x: (genre1 in x) and (genre2 in x))]
    if not filtered_movies.empty:
        movie_names = filtered_movies['original_title'].head(number).tolist()
    else:
        movie_names = None
        
    return movie_names

def main():
    # Streamlit
    st.title('Movie Recommendation System')

    number = st.slider("Select number of movies to recommend", min_value=1, max_value=10, value=5)
    genre1 = st.selectbox('Select prefered genre:', genres_list)
    genre2 = st.selectbox('Select secondary genre:', genres_list)

    filtered_movies = movies_df[movies_df['genres'].apply(lambda x: (genre1 in x) and (genre2 in x))]
    movie_list = filtered_movies['original_title'].tolist()

    # Selector de película
    selected_movie = st.selectbox("Select a movie", movie_list) if movie_list else None

    if not movie_list:
        st.write("No movies available with the selected genres.")
    elif selected_movie:
        st.write(f"Movies similar to {selected_movie}:")
        if st.button("Recommend similar movies"):
            recommended_movies = recommend(number+1, selected_movie)
            if recommended_movies:
                for movie in recommended_movies:
                    st.write(movie)
            else:
                st.write("No similar movies found.")
    else:
        st.warning("Please select a movie to recommend.")

if __name__ == '__main__':
    main()





