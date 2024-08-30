from flask import Flask, request, jsonify
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
                "description": "List of authors",
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
                "description": "Select 1 for Google API or 2 for LLM Generation",
                "default": 1,
            },
        ],
        "responses": {
            200: {
                "description": "A list of recommended books",
                "schema": {
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
                                "type": "integer",
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
                    },
                },
            },
            400: {
                "description": "No arguments were provided",
                "schema": {"type": "array", "items": {"type": "string"}},
            },
            404: {
                "description": "No recommended books found",
                "schema": {"type": "array", "items": {"type": "string"}},
            },
        },
    }
)
@app.route("/book", methods=["GET"])
def book():
    authors = request.args.get("authors", [])
    genres = request.args.get("genres", [])
    use_api = request.args.get("use_api", 1)

    recommended_books = BookService.get_recommendations(
        authors, genres, use_api
    )

    if not recommended_books:
        return (
            jsonify({"error": "No recommended books found"}),
            404,
        )
    return jsonify(recommended_books)
