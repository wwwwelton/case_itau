import requests


class RequestServiceClass:
    def request_google_books(self, authors, genres):
        api_url = "https://www.googleapis.com/books/v1/volumes"

        query_authors = "+".join([f"inauthor:{author}" for author in authors])
        query_genres = "+".join([f"subject:{subject}" for subject in genres])
        query_string = f"{query_authors}+{query_genres}"

        params = {"q": query_string, "maxResults": 20}
        data = requests.get(api_url, params=params)

        return data
