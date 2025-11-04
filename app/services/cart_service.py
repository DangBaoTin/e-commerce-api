# app/services/cart_service.py
from app.models import Product, User, Cart, CartItem
from app.schemas import CartItemCreate
from beanie import PydanticObjectId

from app.services.product_service import product_service, ProductService
from app.repositories.cart_repository import cart_repository, CartRepository

class CartService:
    def __init__(
        self, 
        cart_repo: CartRepository = cart_repository,
        product_srv: ProductService = product_service
    ):
        self.cart_repo = cart_repo
        self.product_srv = product_srv

    async def get_or_create_cart(self, user_id: PydanticObjectId) -> Cart:
        cart = await self.cart_repo.get_by_user_id(user_id)
        if not cart:
            cart = await self.cart_repo.create(user_id)
        return cart

    async def add_item(
        self, 
        user_id: PydanticObjectId, 
        item_in: CartItemCreate
    ) -> Cart | str | None:
        
        # 3. Call the Product Service
        product = await self.product_srv.get_by_id(item_in.product_id)
        if not product:
            return None 
        
        cart = await self.get_or_create_cart(user_id)

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

        if product.stock < new_quantity:
            return "NOT_ENOUGH_STOCK"

        if existing_item:
            existing_item.quantity = new_quantity
        else:
            cart.items.append(CartItem(**item_in.model_dump()))

        await self.cart_repo.update(cart)
        return cart

    async def remove_item(
        self, 
        user_id: PydanticObjectId, 
        product_id: PydanticObjectId
    ) -> Cart | None:
        
        cart = await self.get_or_create_cart(user_id)
        
        item_to_remove = None
        for item in cart.items:
            if item.product_id == product_id:
                item_to_remove = item
                break

        if not item_to_remove:
            return None

        cart.items.remove(item_to_remove)
        await self.cart_repo.update(cart)
        return cart
    
cart_service = CartService()