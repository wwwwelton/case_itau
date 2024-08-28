class Book:
    def __init__(
        self,
        title="",
        subtitle="",
        description="",
        authors=[],
        genres=[],
        language="",
        publisher="",
        published_date=0,
        isbn=0,
        page_count=0,
        buy_link="",
        image_link="",
    ):
        self.title = title
        self.subtitle = subtitle
        self.description = description
        self.authors = authors
        self.genres = genres
        self.language = language
        self.publisher = publisher
        self.published_date = published_date
        self.isbn = isbn
        self.page_count = page_count
        self.buy_link = buy_link
        self.image_link = image_link

    def convert_types(self):
        self.published_date = int(self.published_date)
        self.isbn = int(self.isbn)
        self.page_count = int(self.page_count)

        return self
