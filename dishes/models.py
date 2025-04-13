from beanie import Document, Indexed
from pydantic import BaseModel, model_serializer


class Dish(Document):
    name: str
    price: Indexed(float)
    category: str
    description: str
    quantity: Indexed(float)

    class Settings:
        name = "dishes"

    @model_serializer
    def serialize(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "price": self.price,
            "category": self.category,
            "description": self.description,
            "quantity": self.quantity
        }


class DishUpdateRequest(BaseModel):
    old_value: str | float
    new_value: str | float
    field: str  # "name", "price", "category", "description"
