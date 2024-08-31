from app.application.request_service import RequestServiceClass
from app.domain.models import BookClass
from flask import jsonify, make_response
import requests


class BookService:
    def validate_args(self, authors, genres):
        authors_arguments = True
        genres_arguments = True

        if not authors or all(not element for element in authors):
            authors_arguments = False
        if not genres or all(not element for element in genres):
            genres_arguments = False

        if authors_arguments == False and genres_arguments == False:
            return False
        else:
            return True

    def request_data(self, authors, genres, use_api):
        request_service = RequestServiceClass()

        if use_api == 1:
            data = request_service.request_google_books(authors, genres)

        return data

    def make_books(self, data, use_api):
        if use_api == 1:
            books = BookClass()
            books = books.make_google_books(data)

        return books

    def get_recommendations(self, authors, genres):
        authors = authors.split(",")
        genres = genres.split(",")

        valid_arguments = self.validate_args(authors, genres)
        if valid_arguments == False:
            response_body = {
                "status": "error",
                "message": "No arguments were provided",
                "books": [],
            }
            return make_response(jsonify(response_body), 400)

        data = self.request_data(authors, genres, 1)
        data_json = data.json()

        if data.status_code == 200:
            books = self.make_books(data_json, 1)
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
            response_body = {
                "status": "error",
                "message": data_json.get("error", {}).get("message"),
                "books": [],
            }
            status_code = data_json.get("error", {}).get("code")
            response = make_response(jsonify(response_body), status_code)

        return response
