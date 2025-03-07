from beanie import Document, Indexed


class Dish(Document):
    name: str
    price: Indexed(float)
    category: str

    class Settings:
        name = "dishes"


