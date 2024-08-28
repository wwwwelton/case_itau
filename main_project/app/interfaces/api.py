from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
from app.application.services import BookService

app = Flask(__name__)
swagger = Swagger(app)


@app.route("/books/recommend", methods=["POST"])
@swag_from(
    {
        "responses": {
            200: {
                "description": "Lista de livros recomendados",
                "schema": {"type": "array", "items": {"type": "string"}},
            }
        },
        "parameters": [
            {
                "name": "body",
                "in": "body",
                "required": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "gender": {"type": "string", "example": "masculino"},
                        "favorite_author": {
                            "type": "string",
                            "example": "George Orwell",
                        },
                    },
                },
            }
        ],
    }
)
def recommend_books():
    data = request.get_json()
    gender = data.get("gender")
    favorite_author = data.get("favorite_author")

    recommendations = BookService().get_recommendations(
        gender, favorite_author
    )

    return jsonify(recommendations)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
