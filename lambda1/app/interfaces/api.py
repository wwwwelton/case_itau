from flask import Flask, request
from flasgger import Swagger, swag_from
from app.application.services import BookService

app = Flask(__name__)
swagger = Swagger(app)


@swag_from(
    {
        "parameters": [
            {
                "name": "authors",
                "in": "query",
                "type": "array",
                "items": {"type": "string"},
                "required": False,
                "description": "List of authors of the books",
            },
            {
                "name": "genres",
                "in": "query",
                "type": "array",
                "items": {"type": "string"},
                "required": False,
                "description": "List of genres of the books",
            },
            {
                "name": "use_api",
                "in": "query",
                "type": "integer",
                "required": False,
                "description": "Select 1 for Google API or 2 for Open Library",
                "default": 2,
            },
        ],
        "responses": {
            200: {
                "description": "A list of recommended books",
                "schema": {
                    "type": "object",
                    "properties": {
                        "books": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "title": {
                                        "type": "string",
                                        "description": "Title of the book",
                                    },
                                    "subtitle": {
                                        "type": "string",
                                        "description": "Subtitle of the book, if any",
                                    },
                                    "description": {
                                        "type": "string",
                                        "description": "Brief description of the book",
                                    },
                                    "authors": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "description": "List of authors of the book",
                                    },
                                    "genres": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "description": "List of genres the book belongs to",
                                    },
                                    "languages": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "description": "Languages in which the book is available",
                                    },
                                    "publisher": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "description": "Publishers of the book",
                                    },
                                    "published_date": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "description": "Publication date of the book",
                                    },
                                    "isbn": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "description": "List of ISBN numbers associated with the book",
                                    },
                                    "page_count": {
                                        "type": "string",
                                        "description": "Number of pages in the book",
                                    },
                                    "buy_link": {
                                        "type": "string",
                                        "description": "Link to purchase the book",
                                    },
                                    "image_link": {
                                        "type": "string",
                                        "description": "Link to the book's cover image",
                                    },
                                },
                                "required": [
                                    "title",
                                    "authors",
                                ],
                            },
                        },
                        "message": {"type": "string"},
                        "status": {"type": "string"},
                    },
                },
            },
            400: {
                "description": "Invalid arguments or no arguments were provided",
                "schema": {
                    "type": "object",
                    "properties": {
                        "books": {"type": "array", "items": []},
                        "message": {"type": "string"},
                        "status": {"type": "string"},
                    },
                },
            },
            404: {
                "description": "No recommended books found",
                "schema": {
                    "type": "object",
                    "properties": {
                        "books": {"type": "array", "items": []},
                        "message": {"type": "string"},
                        "status": {"type": "string"},
                    },
                },
            },
            408: {
                "description": "No search API available at this time.",
                "schema": {
                    "type": "object",
                    "properties": {
                        "books": {"type": "array", "items": []},
                        "message": {"type": "string"},
                        "status": {"type": "string"},
                    },
                },
            },
        },
    }
)
@app.route("/", methods=["GET"])
def index():
    authors = request.args.get("authors", "")
    genres = request.args.get("genres", "")
    use_api = request.args.get("use_api", "2")

    recommended_books = BookService()
    recommended_books = recommended_books.get_recommendations(
        authors, genres, use_api
    )

    return recommended_books
