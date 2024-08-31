from app.application.request_service import RequestServiceClass
from app.domain.models import BookClass
from flask import jsonify, make_response


class BookService:
    def validate_args(self, authors, genres, use_api):
        authors_arguments = True
        genres_arguments = True

        if not authors or all(not element for element in authors):
            authors_arguments = False
        if not genres or all(not element for element in genres):
            genres_arguments = False
        if use_api not in {1, 2}:
            return False

        if authors_arguments == False and genres_arguments == False:
            return False
        else:
            return True

    def request_data(self, authors, genres, use_api):
        request_service = RequestServiceClass()

        if use_api == 1:
            data = request_service.request_google_books(authors, genres)
        if use_api == 2:
            data = request_service.request_openlibrary_books(authors, genres)

        return data

    def make_books(self, data, use_api):
        book_obj = BookClass()
        books = []

        if use_api == 1:
            books = book_obj.make_google_books(data)
        if use_api == 2:
            books = book_obj.make_openlibrary_books(data)

        return books

    def get_recommendations(self, authors, genres, use_api):
        authors = authors.split(",")
        genres = genres.split(",")
        use_api = int(use_api) if use_api.isdigit() else -99

        valid_arguments = self.validate_args(authors, genres, use_api)
        if valid_arguments == False:
            response_body = {
                "status": "error",
                "message": "Invalid arguments or no arguments were provided",
                "books": [],
            }
            return make_response(jsonify(response_body), 400)

        data = self.request_data(authors, genres, use_api)
        data_json = data.json()

        if data.status_code == 200:
            books = self.make_books(data_json, use_api)
            if not books:
                response_body = {
                    "status": "error",
                    "message": "No recommended books found",
                    "books": [],
                }
                response = make_response(jsonify(response_body), 404)
            else:
                response_body = {
                    "status": "successful",
                    "message": "Request processed successfully",
                    "books": books,
                }
                response = make_response(jsonify(response_body), 200)
        else:
            message = (
                "No recommended books found"
                if data.status_code == 404
                else data_json.get("error", {}).get("message", "")
            )
            response_body = {
                "status": "error",
                "message": message,
                "books": [],
            }
            status_code = data.status_code
            response = make_response(jsonify(response_body), status_code)

        return response
