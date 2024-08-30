from flask import jsonify, make_response
from app.interfaces.api import app


def lambda_handler(event, context):
    with app.test_request_context(
        path=event["path"],
        method=event["httpMethod"],
        query_string=event.get("queryStringParameters"),
    ):
        data = app.full_dispatch_request()
        response_body = {
            "status": data["status"],
            "message": data["message"],
            "books": data["books"],
        }
        response = make_response(jsonify(response_body), data.status_code)

        return response


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
