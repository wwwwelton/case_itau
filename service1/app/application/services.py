import requests


class BookService:
    def get_recommendations(authors, genres):
        books = []

        authors = authors[0] if authors else []
        authors = [a.split(",") for a in authors]
        genres = genres[0] if genres else []
        genres = [g.split(",") for g in genres]

        for author in authors:
            api_url = f"https://openlibrary.org/search.json?author={author}&sort=new&limit=5"
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                for d in data["docs"]:
                    book = {
                        "title": d.get("title", ""),
                        "subtitle": "",
                        "description": "",
                        "authors": d.get("author_name", []),
                        "genres": d.get("subject", []),
                        "languages": d.get("language", []),
                        "publisher": d.get("publisher", ""),
                        "published_date": d.get("publish_date", 0),
                        "isbn": d.get("isbn", []),
                        "page_count": 0,
                        "buy_link": "",
                        "image_link": "",
                    }
                    books.append(book)
        for genre in genres:
            api_url = f"https://openlibrary.org/search.json?subject={genre}&sort=new&limit=5"
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                for d in data["docs"]:
                    book = {
                        "title": d.get("title", ""),
                        "subtitle": "",
                        "description": "",
                        "authors": d.get("author_name", []),
                        "genres": d.get("subject", []),
                        "languages": d.get("language", []),
                        "publisher": d.get("publisher", ""),
                        "published_date": d.get("publish_date", 0),
                        "isbn": d.get("isbn", []),
                        "page_count": 0,
                        "buy_link": "",
                        "image_link": "",
                    }
                    books.append(book)
        return books
