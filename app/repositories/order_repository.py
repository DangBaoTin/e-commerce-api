from app.models.order import Order
from beanie import PydanticObjectId

class OrderRepository:
    async def create(self, order: Order) -> Order:
        """
        Creates new Order document in the database
        """
        await order.insert()
        return order

    async def get_by_id(self, order_id: PydanticObjectId) -> Order | None:
        """
        Get single order by ID
        """
        return await Order.get(order_id)
    
    async def get_all_for_user(self, user_id: PydanticObjectId) -> list[Order]:
        """
        Get all orders for specific user
        """
        return await Order.find(Order.user_id == user_id).to_list()

order_repository = OrderRepository()