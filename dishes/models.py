from beanie import Document, Indexed
from pydantic import BaseModel


class Dish(Document):
    name: str
    price: Indexed(float)
    category: str
    description: str
    quantity: Indexed(float)

    class Settings:
        name = "dishes"


class DishUpdateRequest(BaseModel):
    old_value: str | float
    new_value: str | float
    field: str  # "name", "price", "category", "description"
