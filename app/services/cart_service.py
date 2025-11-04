# app/services/cart_service.py
from app.models import Product, User, Cart, CartItem
from app.schemas import CartItemCreate
from beanie import PydanticObjectId

from app.repositories.product_repository import product_repository
from app.repositories.cart_repository import cart_repository

class CartService:
    @staticmethod
    async def get_or_create_cart(user_id: PydanticObjectId) -> Cart:
        """
        Retrieves a user's cart or creates a new one if it doesn't exist.
        """
        cart = await cart_repository.get_by_user_id(user_id)
        if not cart:
            cart = await cart_repository.create(user_id)
        return cart

    @staticmethod
    async def add_item(
        user_id: PydanticObjectId, 
        item_in: CartItemCreate
    ) -> Cart | str | None:
        """
        Business logic to add an item to a user's cart.
        """
        # 1. Check if product exists (using the repository)
        product = await product_repository.get(item_in.product_id)
        if not product:
            return None
        
        # 2. Get or create the user's cart
        cart = await CartService.get_or_create_cart(user_id)

        # 3. Check if item is already in cart
        existing_item = None
        for item in cart.items:
            if item.product_id == item_in.product_id:
                existing_item = item
                break
        new_quantity = 0
        if existing_item:
            new_quantity = existing_item.quantity + item_in.quantity
        else:
            new_quantity = item_in.quantity

        # 4. Check stock
        if product.stock < new_quantity:
            return "NOT_ENOUGH_STOCK"

        # 5. Update cart logic
        if existing_item:
            existing_item.quantity = new_quantity
        else:
            cart.items.append(CartItem(**item_in.model_dump()))

        await cart_repository.update(cart)
        return cart

    @staticmethod
    async def remove_item(
        user_id: PydanticObjectId, 
        product_id: PydanticObjectId
    ) -> Cart | None:
        """
        Business logic to remove an item from a user's cart.
        """
        cart = await CartService.get_or_create_cart(user_id)

        item_to_remove = None
        for item in cart.items:
            if item.product_id == product_id:
                item_to_remove = item
                break

        if not item_to_remove:
            return None

        cart.items.remove(item_to_remove)
        
        # 4. Use the repository to save
        await cart_repository.update(cart)
        return cart