# app/repositories/cart_repository.py
from app.models import Cart, CartItem
from beanie import PydanticObjectId

class CartRepository:
    """
    This class handles all database operations for the Cart model.
    """

    async def get_by_user_id(self, user_id: PydanticObjectId) -> Cart | None:
        """
        Get a cart by its user_id.
        """
        return await Cart.find_one(Cart.user_id == user_id)

    async def create(self, user_id: PydanticObjectId) -> Cart:
        """
        Create a new, empty cart for a user.
        """
        cart = Cart(user_id=user_id, items=[])
        await cart.insert()
        return cart

    async def update(self, cart: Cart) -> Cart:
        """
        Save any changes to a cart document.
        """
        await cart.save()
        return cart

# Create a single instance
cart_repository = CartRepository()