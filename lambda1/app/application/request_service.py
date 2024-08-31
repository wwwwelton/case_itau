from flask import json
import requests
import os


class RequestServiceClass:
    def request_google_books(self, authors, genres):
        api_url = "https://www.googleapis.com/books/v1/volumes"

        query_authors = "+".join([f"inauthor:{author}" for author in authors])
        query_genres = "+".join([f"subject:{subject}" for subject in genres])
        query_string = f"{query_authors}+{query_genres}"

        params = {
            "q": query_string,
            "maxResults": 20,
            "key": os.getenv("GOOGLE_API"),
        }
        data = requests.get(api_url, params=params)

        return data

    def request_openlibrary_books(self, authors, genres):
        api_url = "https://openlibrary.org/search.json?"
        data = []

        for author in authors:
            limit = 10 if len(authors) / 10 < 1 else len(authors) / 10
            params = {"author": author, "sort": "new", "limit": limit}
            response = requests.get(api_url, params=params)
            if response.status_code != 200:
                continue

            data.append(response.json().get("docs", []))

        for genre in genres:
            limit = 10 if len(genres) / 10 < 1 else len(genres) / 10
            params = {"subject": genre, "sort": "new", "limit": limit}
            response = requests.get(api_url, params=params)
            if response.status_code != 200:
                continue

            data.append(response.json().get("docs", []))

        fake_requests = requests.get(api_url, {"q": "twain"})
        fake_requests.body = json.dumps(data)
        data = fake_requests

        return data
