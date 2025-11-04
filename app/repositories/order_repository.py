# app/repositories/order_repository.py
from app.models.order import Order
from app.models.cart import Cart
from beanie import PydanticObjectId

class OrderRepository:
    """
    This class handles all database operations for the Order model.
    """
    async def create(self, order: Order) -> Order:
        """
        Creates a new Order document in the database.
        """
        await order.insert()
        return order

    async def get_by_id(self, order_id: PydanticObjectId) -> Order | None:
        """
        Get a single order by its ID.
        """
        return await Order.get(order_id)
    
    async def get_all_for_user(self, user_id: PydanticObjectId) -> list[Order]:
        """
        Get all orders for a specific user.
        """
        return await Order.find(Order.user_id == user_id).to_list()

# Create a single instance
order_repository = OrderRepository()