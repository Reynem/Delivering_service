from beanie import Document, Indexed, PydanticObjectId
from pydantic import EmailStr, BaseModel


class Cart(Document):
    user_email: EmailStr
    dish_id: PydanticObjectId
    quantity: Indexed(int)

    class Settings:
        name = "carts"
        use_state_management = True


class CartIn(BaseModel):
    dish_name: str
    price: float
    category: str
    quantity: int
