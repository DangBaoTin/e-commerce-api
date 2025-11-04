# app/api/v1/endpoints/cart.py
from fastapi import APIRouter, Depends, HTTPException, status

from app.models.user import User
from app.models.cart import Cart

from app.schemas.cart import CartItemCreate, CartOut
from app.api.dependencies import get_current_user

from beanie import PydanticObjectId

from app.services.cart_service import cart_service

router = APIRouter()

async def get_or_create_cart(user_id: PydanticObjectId) -> Cart:
    """
    Utility function to get a user's cart or create one if it doesn't exist.
    """
    cart = await Cart.find_one(Cart.user_id == user_id)
    if not cart:
        cart = Cart(user_id=user_id, items=[])
        await cart.insert()
    return cart

@router.post("/items", response_model=CartOut)
async def add_item_to_cart(
    item_in: CartItemCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Add a product to the current user's shopping cart.
    
    If the item is already in the cart, its quantity is increased.
    """
    user_id = current_user.id
    
    # 2. Call the service instance
    cart_or_error = await cart_service.add_item(user_id, item_in) # pyright: ignore[reportArgumentType]
    
    if cart_or_error is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    if cart_or_error == "NOT_ENOUGH_STOCK":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough stock"
        )

    return CartOut(
        id=str(cart_or_error.id), # type: ignore
        user_id=cart_or_error.user_id, # type: ignore
        items=cart_or_error.items # type: ignore
    )

@router.get("/", response_model=CartOut)
async def get_user_cart(
    current_user: User = Depends(get_current_user)
):
    """
    Get the current user's shopping cart.
    """
    cart = await cart_service.get_or_create_cart(current_user.id) # type: ignore
    
    return CartOut(
        id=str(cart.id),
        user_id=cart.user_id,
        items=cart.items # type: ignore
    )

@router.delete("/items/{product_id}", response_model=CartOut)
async def remove_item_from_cart(
    product_id: PydanticObjectId,
    current_user: User = Depends(get_current_user)
):
    """
    Remove a product from the current user's shopping cart.
    """
    user_id = current_user.id  # type: ignore
    
    # 4. Call the service instance
    cart = await cart_service.remove_item(user_id, product_id) # pyright: ignore[reportArgumentType]
    
    if cart is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found in cart"
        )

    return CartOut(
        id=str(cart.id),
        user_id=cart.user_id,
        items=cart.items # type: ignore
    )