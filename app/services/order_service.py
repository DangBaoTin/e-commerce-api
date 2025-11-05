import stripe
from beanie import PydanticObjectId
from app.core.config import settings
from app.models.order import Order
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
        Create a new order from the user cart
        """
        # Get the user's cart
        cart = await self.cart_repo.get_by_user_id(user_id)
        if not cart or not cart.items:
            return "CART_EMPTY"

        total_price = 0.0
        order_items = []
        products_to_update = []

        # Check stock and get prices for all items
        for item in cart.items:
            product = await self.product_repo.get(item.product_id)
            
            if not product:
                return "PRODUCT_NOT_FOUND"
            
            if product.stock < item.quantity:
                return "NOT_ENOUGH_STOCK"
            
            price_at_purchase = product.price
            total_price += item.quantity * price_at_purchase
            
            order_items.append({
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price_at_purchase": price_at_purchase
            })
            
            product.stock -= item.quantity
            products_to_update.append(product)

        order = Order(
            user_id=user_id,
            items=order_items,
            total_price=total_price
        )
        await self.order_repo.create(order)
        
        # Update product stocks
        for product in products_to_update:
            await self.product_repo.save(product)

        # Clear the cart
        cart.items = []
        await self.cart_repo.update(cart)

        return order
    
    async def create_checkout_session(
        self, 
        user_id: PydanticObjectId
    ) -> dict | str:
        """
        Creates a Stripe Checkout Session for the user's cart.
        """
        # 1. Get the user's cart
        cart = await self.cart_repo.get_by_user_id(user_id)
        if not cart or not cart.items:
            return "CART_EMPTY"

        # 2. Build the 'line_items' for Stripe
        line_items = []
        for item in cart.items:
            product = await self.product_repo.get(item.product_id)
            if not product:
                return "PRODUCT_NOT_FOUND"
            
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product.name,
                    },
                    # Price must be in cents!
                    'unit_amount': int(product.price * 100),
                },
                'quantity': item.quantity,
            })

        # Define success and cancel URLs
        success_url = f"http://localhost:8000/payment-success?user_id={user_id}"
        cancel_url = "http://localhost:8000/payment-cancelled"

        # Create the Stripe Checkout Session
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=success_url,
                cancel_url=cancel_url,
                metadata={
                    "user_id": str(user_id)
                }
            )
            return {"url": session.url}
        except Exception as e:
            print(f"Error creating Stripe session: {e}")
            return "STRIPE_ERROR"

order_service = OrderService()