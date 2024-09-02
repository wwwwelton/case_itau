from flask import json
import requests
import os
from requests.models import Response


class RequestServiceClass:
    def request_google_books(self, authors, genres):
        api_url = "https://www.googleapis.com/books/v1/volumes"
        items = []

        limit = len(authors) + len(genres)
        limit = 20 if limit / 10 < 1 else len(limit) / 10

        for author in authors:
            params = {"q": f"inauthor:{author}", "maxResults": limit}
            if os.getenv("GOOGLE_API"):
                params["key"] = os.getenv("GOOGLE_API")
            response = requests.get(api_url, params=params)
            if response.status_code != 200:
                continue

            items.extend(response.json().get("items", []))

        for genre in genres:
            params = {"q": f"subject:{genre}", "maxResults": limit}
            if os.getenv("GOOGLE_API"):
                params["key"] = os.getenv("GOOGLE_API")
            response = requests.get(api_url, params=params)
            if response.status_code != 200:
                continue

            items.extend(response.json().get("items", []))

        data = Response()
        data.status_code = 200 if items else 404
        data._content = json.dumps({"items": items}).encode("utf-8")
        data.headers["Content-Type"] = "application/json"

        return data

    def request_openlibrary_books(self, authors, genres):
        api_url = "https://openlibrary.org/search.json?"
        docs = []

        limit = len(authors) + len(genres)
        limit = 20 if limit / 10 < 1 else len(limit) / 10

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
