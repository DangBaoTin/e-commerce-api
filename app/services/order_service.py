# app/services/order_service.py
from app.models.order import Order
from app.models.cart import Cart, CartItem
from app.schemas.cart import CartItemCreate
from beanie import PydanticObjectId
from app.services.cart_service import cart_service, CartService
from app.services.product_service import product_service, ProductService
from app.repositories.order_repository import order_repository, OrderRepository
from app.repositories.product_repository import product_repository, ProductRepository
from app.repositories.cart_repository import cart_repository, CartRepository

class OrderService:
    def __init__(
        self,
        order_repo: OrderRepository = order_repository,
        cart_repo: CartRepository = cart_repository,
        product_repo: ProductRepository = product_repository
    ):
        self.order_repo = order_repo
        self.cart_repo = cart_repo
        self.product_repo = product_repo

    async def create_order_from_cart(
        self, 
        user_id: PydanticObjectId
    ) -> Order | str:
        """
        Create a new order from the user's cart.
        Returns the new Order or an error string.
        """
        # 1. Get the user's cart
        cart = await self.cart_repo.get_by_user_id(user_id)
        if not cart or not cart.items:
            return "CART_EMPTY"

        total_price = 0.0
        order_items = []
        products_to_update = []

        # 2. Check stock and get prices for all items
        for item in cart.items:
            product = await self.product_repo.get(item.product_id)
            
            if not product:
                return "PRODUCT_NOT_FOUND"
            
            if product.stock < item.quantity:
                return "NOT_ENOUGH_STOCK"
            
            # 3. Calculate total and build order items
            price_at_purchase = product.price
            total_price += item.quantity * price_at_purchase
            
            order_items.append({
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price_at_purchase": price_at_purchase
            })
            
            # 4. Prepare product for stock update
            product.stock -= item.quantity
            products_to_update.append(product)

        # 5. Create the order
        order = Order(
            user_id=user_id,
            items=order_items, # type: ignore
            total_price=total_price
        )
        await self.order_repo.create(order) # 'create' should be a method in OrderRepository

        # 6. Update stock for all products
        for product in products_to_update:
            # We need an update method in the ProductRepository for this
            # Let's assume one exists or we just save the product
            await self.product_repo.save(product) # We'll need to add a 'save' method

        # 7. Clear the cart
        cart.items = []
        await self.cart_repo.update(cart)

        # 8. Return the new order
        return order

# Create a single instance
order_service = OrderService()