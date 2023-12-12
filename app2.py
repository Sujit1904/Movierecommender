import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    try:
        url = "https://api.themoviedb.org/3/movie/{}?api_key=93c0360f9a2c3670d9c4acdc3f974e28&language=en-US".format(movie_id)
        data = requests.get(url)
        data.raise_for_status()  # Raise an exception for HTTP errors (e.g., 404)
        data = data.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    except Exception as e:
        st.error(f"Error fetching movie poster")
        return None

def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []
        for i in distances[1:6]:
            # fetch the movie poster
            movie_id = movies.iloc[i[0]].movie_id
            poster = fetch_poster(movie_id)
            if poster:
                recommended_movie_posters.append(poster)
                recommended_movie_names.append(movies.iloc[i[0]].title)

        return recommended_movie_names, recommended_movie_posters
    except Exception as e:
        st.error(f"Error recommending movies")
        return None, None

# Load movie data and similarity matrix
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('simalirity.pkl', 'rb'))

# Set page title and styling
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide",
)

# Custom styling
st.markdown(
    """
    <style>
        body {
            background-color: #3498db; /* Background color */
            color: #3498db; /* Text color */
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
        }
        h1 {
            color: #3498db; /* Title color */
            text-align: center;
        }
        .stButton {
            background-color: #3498db;
            color: white;
            padding: 15px 20px;
            font-size: 18px;
            border: none;
            border-radius: 5px;
            margin-top: 20px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .stButton:hover {
            background-color: #2980b9;
        }
        .recommendation-container {
            display: flex;
            overflow-x: auto;
            padding: 10px;
            justify-content: space-between;
            margin-top: 20px;
        }
        .movie-card {
            width: 200px;
            text-align: center;
            margin: 10px;
            padding: 10px;
            background-color: #fff;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            border-radius: 10px;
            transition: transform 0.3s ease;
        }
        .movie-card:hover {
            transform: scale(1.05);
        }
        .movie-card img {
            width: 100%;
            border-radius: 5px;
            margin-top: 10px;
        }
        .selectbox-container {
            width: 50%;
            margin: 20px auto;
        }
        .main-container {
            max-width: 1200px;
            margin: auto;
            padding: 20px;
        }
        .header-container {
            margin-bottom: 30px;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# Page layout
with st.container():
    # Page header
    st.markdown('<h1 style="color: #000000; text-align: center;">Movie Recommender System</h1>', unsafe_allow_html=True)

    # Header container
    with st.container():
        movie_list = movies['title'].values
        selected_movie = st.selectbox(
            "Type or select a movie from the dropdown",
            movie_list,
            key='movie_selectbox'
        )

    # Main container
    with st.container():
        # Show Recommendation button
        button_html = (
            f'<button style="background-color: #3498db; color: white; padding: 15px 20px; font-size: 18px; border: none; border-radius: 5px; margin-top: 20px; cursor: pointer; transition: background-color 0.3s ease;">'
            'Show Recommendation'
            '</button>'
        )

        if st.markdown(button_html, unsafe_allow_html=True):
            recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

            if recommended_movie_names is not None and recommended_movie_posters is not None:
                # Display recommended movies horizontally
                st.markdown('<h2 style="color: #000000; font-weight: bold;text-align: center;">Recommended Movies</h2>', unsafe_allow_html=True)

                # Use a single row to display the posters horizontally
                col1 = st.columns(len(recommended_movie_names))
                
                for name, poster, col in zip(recommended_movie_names, recommended_movie_posters, col1):
                    with col:
                      styled_name = f'<span style="font-family: Arial, sans-serif; font-size: 18px; color:#000000;">{name}</span>'
                      st.markdown(styled_name, unsafe_allow_html=True)
                      print(name)
                      st.image(poster, use_column_width=True)