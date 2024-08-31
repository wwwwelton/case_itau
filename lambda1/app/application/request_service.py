from flask import json
import requests
import os
from requests.models import Response


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
        if os.getenv("GOOGLE_API"):
            params["key"] = os.getenv("GOOGLE_API")

        data = requests.get(api_url, params=params)

        return data

    def request_openlibrary_books(self, authors, genres):
        api_url = "https://openlibrary.org/search.json?"
        docs = []

        limit = len(authors) + len(genres)
        limit = 10 if limit / 10 < 1 else len(limit) / 10

        for author in authors:
            params = {"author": author, "sort": "new", "limit": limit}
            response = requests.get(api_url, params=params)
            if response.status_code != 200:
                continue

            docs.extend(response.json().get("docs", []))

        for genre in genres:
            params = {"subject": genre, "sort": "new", "limit": limit}
            response = requests.get(api_url, params=params)
            if response.status_code != 200:
                continue

            docs.extend(response.json().get("docs", []))

        data = Response()
        data.status_code = 200 if docs else 404
        data._content = json.dumps({"docs": docs}).encode("utf-8")
        data.headers["Content-Type"] = "application/json"

        return data
