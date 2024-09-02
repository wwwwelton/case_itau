class BookClass:
    def __init__(self, *args, **kwargs):
        self.title = kwargs.get("title", "")
        self.subtitle = kwargs.get("subtitle", "")
        self.description = kwargs.get("description", "")
        self.authors = kwargs.get("authors", [])
        self.genres = kwargs.get("genres", [])
        self.language = kwargs.get("language", [])
        self.publisher = kwargs.get("publisher", "")
        self.published_date = kwargs.get("published_date", "")
        self.isbn = kwargs.get("isbn", [])
        self.page_count = kwargs.get("page_count", "")
        self.buy_link = kwargs.get("buy_link", "")
        self.image_link = kwargs.get("image_link", "")

    def to_dict(self):
        return {
            "title": self.title,
            "subtitle": self.subtitle,
            "description": self.description,
            "authors": self.authors,
            "genres": self.genres,
            "language": self.language,
            "publisher": self.publisher,
            "published_date": self.published_date,
            "isbn": self.isbn,
            "page_count": self.page_count,
            "buy_link": self.buy_link,
            "image_link": self.image_link,
        }

    def make_google_books(self, data):
        books = []

        for item in data.get("items", []):
            volume_info = item.get("volumeInfo", {})
            sale_info = item.get("saleInfo", {})

            book = BookClass(
                title=volume_info.get("title", ""),
                subtitle=volume_info.get("subtitle", ""),
                description=volume_info.get("description", ""),
                authors=volume_info.get("authors", []),
                genres=volume_info.get("categories", []),
                language=volume_info.get("language", []),
                publisher=volume_info.get("publisher", ""),
                published_date=volume_info.get("publishedDate", ""),
                isbn=volume_info.get("industryIdentifiers", []),
                page_count=volume_info.get("pageCount", ""),
                buy_link=sale_info.get("buyLink", ""),
                image_link=volume_info.get("imageLinks", {}).get(
                    "thumbnail", ""
                ),
            )

            books.append(book.to_dict())

        return books

    def make_openlibrary_books(self, data):
        books = []
        amz_store = "https://www.amazon.com.br/dp/"
        cover_url = "https://covers.openlibrary.org/b/id/"

        for doc in data.get("docs", []):
            book = BookClass(
                title=doc.get("title", ""),
                subtitle=doc.get("title_suggest", ""),
                description=doc.get("first_sentence", ""),
                authors=doc.get("author_name", []),
                genres=doc.get("subject", []),
                language=doc.get("language", []),
                publisher=doc.get("publisher", ""),
                published_date=doc.get("publish_year", ""),
                isbn=doc.get("isbn", []),
                page_count=doc.get("number_of_pages_median", ""),
                buy_link=f"{amz_store}{doc.get('buyLink', '')}",
                image_link=f"{cover_url}{doc.get('cover_i', '')}.jpg",
            )

            books.append(book.to_dict())

        return books
