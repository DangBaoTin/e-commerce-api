# app/api/v1/endpoints/orders.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user import User
from app.schemas.order import OrderOut, OrderItemOut
from app.api.dependencies import get_current_user
from app.services.order_service import order_service

router = APIRouter()

@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def create_order(
    current_user: User = Depends(get_current_user)
):
    """
    Create a new order from the user's current shopping cart.
    """
    user_id = current_user.id  # type: ignore
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found."
        )
    
    order_or_error = await order_service.create_order_from_cart(user_id)
    
    # Handle error responses from the service
    if isinstance(order_or_error, str):
        error_detail = "Could not create order."
        if order_or_error == "CART_EMPTY":
            error_detail = "Your cart is empty."
        elif order_or_error == "PRODUCT_NOT_FOUND":
            error_detail = "An item in your cart was not found."
        elif order_or_error == "NOT_ENOUGH_STOCK":
            error_detail = "An item in your cart is out of stock."
            
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_detail
        )
    
    # Manually build the response
    return OrderOut(
        id=str(order_or_error.id),
        user_id=order_or_error.user_id,
        items=[OrderItemOut.model_validate(item) for item in order_or_error.items],
        total_price=order_or_error.total_price,
        order_status=order_or_error.order_status,
        created_at=order_or_error.created_at
    )