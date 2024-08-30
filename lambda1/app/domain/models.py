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
