from beanie import Document, Indexed
from pydantic import EmailStr, BaseModel


class Cart(Document):
    user_email: EmailStr
    dish_name: str
    price: Indexed(float)
    category: str
    quantity: Indexed(float)

    class Settings:
        name = "carts"
        use_state_management = True


class CartIn(BaseModel):
    dish_name: str
    price: float
    category: str
    quantity: float
