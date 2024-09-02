from flask.cli import load_dotenv
from app.interfaces.api import app

load_dotenv()


def lambda_handler(event, context):
    with app.test_request_context(
        path=event["path"],
        method=event["httpMethod"],
        query_string=event.get("queryStringParameters"),
    ):
        response = app.full_dispatch_request()

        return {
            "statusCode": response.status_code,
            "body": response.get_data(as_text=True),
            "headers": dict(response.headers),
        }


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
