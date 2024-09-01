import os

from flask import json
from openai import OpenAI


class LlmServiceClass:
    @staticmethod
    def llm_improve_result(books):
        if os.getenv("OPENAI_API_KEY"):
            client = OpenAI()
        else:
            return books

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": [
                            {
                                "type": "text",
                                "text": 'Act like a renowned book critic, you have knowledge of all literary works, authors and genres.\nYou will receive an array of books resulting from a python function, rearrange the books so that the best books are at the beginning.\nDo not change the name of the keys.\nKeep the text in same provided language.\nThe response must be a valid JSON.\nIf you have more than 10 books, limit the results to the top 10. If you have multiple authors and genres, use half of the top ones based on genre and the other half based on author.\nMake the following adjustments if necessary to the key values:\n"title": Convert to camel case\n"subtitle": Convert to camel case\n"description": Adjust the text to a more cohesive format\n"authors": Convert to camel case\n"genres": Convert to camel case\n"languages": Convert to ISO 639 language format\n"publisher": Convert to camel case\n"published_date": Extract only the year',
                            }
                        ],
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(books),
                            }
                        ],
                    },
                ],
                temperature=0,
                max_tokens=16383,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                response_format={"type": "json_object"},
            )
            raw_books = json.loads(response.choices[0].message.content)[
                "books"
            ]
            if raw_books:
                books = raw_books
        except:
            return books

        return books
