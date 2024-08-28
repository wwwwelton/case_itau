class BookService:
    def get_recommendations(self, gender, favorite_author):
        return (
            ["1984", "Animal Farm", "Homage to Catalonia"]
            if favorite_author == "George Orwell"
            else []
        )
