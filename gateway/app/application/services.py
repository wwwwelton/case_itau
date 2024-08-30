from flask import jsonify, make_response
import requests

data1 = {
    "books": [
        {
            "title": "To Kill a Mockingbird",
            "subtitle": "",
            "description": "",
            "authors": ["Harper Lee"],
            "genres": ["Fiction", "Classic"],
            "languages": ["English"],
            "publisher": "J.B. Lippincott & Co.",
            "published_date": 1960,
            "isbn": ["9780061120084"],
            "page_count": 281,
            "buy_link": "",
            "image_link": "",
        },
        {
            "title": "1984",
            "subtitle": "",
            "description": "",
            "authors": ["George Orwell"],
            "genres": ["Dystopian", "Science Fiction"],
            "languages": ["English"],
            "publisher": "Secker & Warburg",
            "published_date": 1949,
            "isbn": ["9780451524935"],
            "page_count": 328,
            "buy_link": "",
            "image_link": "",
        },
        {
            "title": "The Great Gatsby",
            "subtitle": "",
            "description": "",
            "authors": ["F. Scott Fitzgerald"],
            "genres": ["Fiction", "Classic"],
            "languages": ["English"],
            "publisher": "Charles Scribner's Sons",
            "published_date": 1925,
            "isbn": ["9780743273565"],
            "page_count": 180,
            "buy_link": "",
            "image_link": "",
        },
        {
            "title": "Pride and Prejudice",
            "subtitle": "",
            "description": "",
            "authors": ["Jane Austen"],
            "genres": ["Romance", "Classic"],
            "languages": ["English"],
            "publisher": "T. Egerton",
            "published_date": 1813,
            "isbn": ["9780141439518"],
            "page_count": 279,
            "buy_link": "",
            "image_link": "",
        },
        {
            "title": "Moby-Dick",
            "subtitle": "",
            "description": "",
            "authors": ["Herman Melville"],
            "genres": ["Adventure", "Classic"],
            "languages": ["English"],
            "publisher": "Harper & Brothers",
            "published_date": 1851,
            "isbn": ["9781503280786"],
            "page_count": 585,
            "buy_link": "",
            "image_link": "",
        },
        {
            "title": "War and Peace",
            "subtitle": "",
            "description": "",
            "authors": ["Leo Tolstoy"],
            "genres": ["Historical", "Classic"],
            "languages": ["Russian"],
            "publisher": "The Russian Messenger",
            "published_date": 1869,
            "isbn": ["9780199232765"],
            "page_count": 1225,
            "buy_link": "",
            "image_link": "",
        },
        {
            "title": "The Catcher in the Rye",
            "subtitle": "",
            "description": "",
            "authors": ["J.D. Salinger"],
            "genres": ["Fiction", "Classic"],
            "languages": ["English"],
            "publisher": "Little, Brown and Company",
            "published_date": 1951,
            "isbn": ["9780316769488"],
            "page_count": 214,
            "buy_link": "",
            "image_link": "",
        },
        {
            "title": "The Hobbit",
            "subtitle": "",
            "description": "",
            "authors": ["J.R.R. Tolkien"],
            "genres": ["Fantasy", "Adventure"],
            "languages": ["English"],
            "publisher": "George Allen & Unwin",
            "published_date": 1937,
            "isbn": ["9780547928227"],
            "page_count": 310,
            "buy_link": "",
            "image_link": "",
        },
        {
            "title": "Crime and Punishment",
            "subtitle": "",
            "description": "",
            "authors": ["Fyodor Dostoevsky"],
            "genres": ["Philosophical Fiction", "Classic"],
            "languages": ["Russian"],
            "publisher": "The Russian Messenger",
            "published_date": 1866,
            "isbn": ["9780140449136"],
            "page_count": 671,
            "buy_link": "",
            "image_link": "",
        },
        {
            "title": "The Odyssey",
            "subtitle": "",
            "description": "",
            "authors": ["Homer"],
            "genres": ["Epic", "Classic"],
            "languages": ["Ancient Greek"],
            "publisher": "Unknown",
            "published_date": -800,
            "isbn": ["9780140268867"],
            "page_count": 541,
            "buy_link": "",
            "image_link": "",
        },
    ],
    "message": "Request processed successfully",
    "status": "successful",
}

data2 = {
    "books": [
        {
            "title": "Brave New World",
            "subtitle": "",
            "description": "",
            "authors": ["Aldous Huxley"],
            "genres": ["Dystopian", "Science Fiction"],
            "languages": ["English"],
            "publisher": "Chatto & Windus",
            "published_date": 1932,
            "isbn": ["9780060850524"],
            "page_count": 268,
            "buy_link": "",
            "image_link": "",
        },
        {
            "title": "The Lord of the Rings",
            "subtitle": "",
            "description": "",
            "authors": ["J.R.R. Tolkien"],
            "genres": ["Fantasy", "Adventure"],
            "languages": ["English"],
            "publisher": "George Allen & Unwin",
            "published_date": 1954,
            "isbn": ["9780544003415"],
            "page_count": 1178,
            "buy_link": "",
            "image_link": "",
        },
        {
            "title": "The Brothers Karamazov",
            "subtitle": "",
            "description": "",
            "authors": ["Fyodor Dostoevsky"],
            "genres": ["Philosophical Fiction", "Classic"],
            "languages": ["Russian"],
            "publisher": "The Russian Messenger",
            "published_date": 1880,
            "isbn": ["9780374528379"],
            "page_count": 796,
            "buy_link": "",
            "image_link": "",
        },
        {
            "title": "Jane Eyre",
            "subtitle": "",
            "description": "",
            "authors": ["Charlotte Brontë"],
            "genres": ["Gothic", "Romance"],
            "languages": ["English"],
            "publisher": "Smith, Elder & Co.",
            "published_date": 1847,
            "isbn": ["9780141441146"],
            "page_count": 532,
            "buy_link": "",
            "image_link": "",
        },
        {
            "title": "The Catch-22",
            "subtitle": "",
            "description": "",
            "authors": ["Joseph Heller"],
            "genres": ["Satire", "War"],
            "languages": ["English"],
            "publisher": "Simon & Schuster",
            "published_date": 1961,
            "isbn": ["9780684833392"],
            "page_count": 453,
            "buy_link": "",
            "image_link": "",
        },
        {
            "title": "Anna Karenina",
            "subtitle": "",
            "description": "",
            "authors": ["Leo Tolstoy"],
            "genres": ["Romance", "Classic"],
            "languages": ["Russian"],
            "publisher": "The Russian Messenger",
            "published_date": 1877,
            "isbn": ["9780143035008"],
            "page_count": 864,
            "buy_link": "",
            "image_link": "",
        },
        {
            "title": "The Divine Comedy",
            "subtitle": "",
            "description": "",
            "authors": ["Dante Alighieri"],
            "genres": ["Epic", "Poetry"],
            "languages": ["Italian"],
            "publisher": "Unknown",
            "published_date": 1320,
            "isbn": ["9780140448955"],
            "page_count": 798,
            "buy_link": "",
            "image_link": "",
        },
        {
            "title": "Don Quixote",
            "subtitle": "",
            "description": "",
            "authors": ["Miguel de Cervantes"],
            "genres": ["Adventure", "Classic"],
            "languages": ["Spanish"],
            "publisher": "Francisco de Robles",
            "published_date": 1605,
            "isbn": ["9780060934347"],
            "page_count": 1072,
            "buy_link": "",
            "image_link": "",
        },
        {
            "title": "One Hundred Years of Solitude",
            "subtitle": "",
            "description": "",
            "authors": ["Gabriel García Márquez"],
            "genres": ["Magical Realism", "Fiction"],
            "languages": ["Spanish"],
            "publisher": "Harper & Row",
            "published_date": 1967,
            "isbn": ["9780060883287"],
            "page_count": 417,
            "buy_link": "",
            "image_link": "",
        },
        {
            "title": "Wuthering Heights",
            "subtitle": "",
            "description": "",
            "authors": ["Emily Brontë"],
            "genres": ["Gothic", "Romance"],
            "languages": ["English"],
            "publisher": "Thomas Cautley Newby",
            "published_date": 1847,
            "isbn": ["9780141439556"],
            "page_count": 416,
            "buy_link": "",
            "image_link": "",
        },
    ],
    "message": "Request processed successfully",
    "status": "successful",
}


class BookService:
    def validate_args(self, authors, genres, use_api):
        if not authors or all(not element for element in authors):
            return (False, "authors", authors)
        if not genres or all(not element for element in genres):
            return (False, "genres", genres)
        if use_api not in {1, 2}:
            if use_api == -99:
                use_api = ""
            return (False, "use_api", use_api)
        return (True, "", "")

    def get_recommendations(self, authors, genres, use_api):
        authors = authors.split(",")
        genres = genres.split(",")
        use_api = int(use_api)

        valid_arguments = self.validate_args(authors, genres, use_api)
        if valid_arguments[0] == False:
            response_body = {
                "status": "error",
                "message": f"Invalid argument: {valid_arguments[1]} cannot be {valid_arguments[2]}",
                "books": [],
            }
            return make_response(jsonify(response_body), 400)

        if use_api == 1:
            response_body = {
                "status": data1["status"],
                "message": data1["message"],
                "books": data1["books"],
            }
            response = make_response(jsonify(response_body), 200)
        elif use_api == 2:
            response_body = {
                "status": data2["status"],
                "message": data2["message"],
                "books": data2["books"],
            }
            response = make_response(jsonify(response_body), 200)
        else:
            response_body = {
                "status": "error",
                "message": "No recommended books found",
                "books": [],
            }
            response = make_response(jsonify(response_body), 400)

        return response
