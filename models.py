from beanie import Document


class Dish(Document):
    name: str
    price: float
    category: str

    class Settings:
        name = "dishes"


