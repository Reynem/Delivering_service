from beanie import Document, Indexed
from pydantic import EmailStr


class Cart(Document):
    user_email: EmailStr
    dish_name: str
    price: Indexed(float)
    category: str
    quantity: Indexed(float)

    class Settings:
        name = "dishes"
