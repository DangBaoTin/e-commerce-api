from app.models.cart import Cart
from beanie import PydanticObjectId

class CartRepository:
    async def get_by_user_id(self, user_id: PydanticObjectId) -> Cart | None:
        """
        Get cart by user_id
        """
        return await Cart.find_one(Cart.user_id == user_id)

    async def create(self, user_id: PydanticObjectId) -> Cart:
        """
        Create new cart for user
        """
        cart = Cart(user_id=user_id, items=[])
        await cart.insert()
        return cart

    async def update(self, cart: Cart) -> Cart:
        """
        Save changes to cart document
        """
        await cart.save()
        return cart

cart_repository = CartRepository()