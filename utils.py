import requests

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
    if res["Response"] == "True":
        return {
            "title": res["Title"],
            "year": res["Year"],
            "poster": res["Poster"],
            "rating": res["imdbRating"],
            "genre": res["Genre"],
            "plot": res["Plot"]
        }
    return None
