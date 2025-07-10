import requests
from difflib import get_close_matches

def readable_size(size_in_bytes):
    if size_in_bytes < 1024:
        return f"{size_in_bytes} B"
    elif size_in_bytes < 1024 ** 2:
        return f"{size_in_bytes / 1024:.2f} KB"
    elif size_in_bytes < 1024 ** 3:
        return f"{size_in_bytes / (1024 ** 2):.2f} MB"
    else:
        return f"{size_in_bytes / (1024 ** 3):.2f} GB"

def fetch_imdb_details(title):
    url = f"https://www.omdbapi.com/?t={title}&apikey=your_omdb_api_key"
    res = requests.get(url).json()
    if res.get("Response") == "True":
        return {
            "title": res["Title"],
            "year": res["Year"],
            "poster": res["Poster"],
            "rating": res["imdbRating"],
            "genre": res["Genre"],
            "plot": res["Plot"]
        }
    return None

def get_similar_titles(query):
    # Replace this list with your actual index of titles from your DB or cache
    all_titles = [
        "Avengers Endgame",
        "Avatar The Way of Water",
        "Inception",
        "Interstellar",
        "Iron Man 3",
        "The Dark Knight",
        "Spider-Man No Way Home",
        "Pushpa",
        "RRR",
        "KGF Chapter 2"
    ]
    return get_close_matches(query, all_titles, n=3, cutoff=0.6)
