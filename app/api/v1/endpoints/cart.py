# app/api/v1/endpoints/cart.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.models import Product, User, Cart, CartItem
from app.schemas import CartItemCreate, CartOut
from app.api.dependencies import get_current_user
from beanie import PydanticObjectId

from app.services.cart_service import CartService

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
    user_id = current_user.id  # type: ignore
    
    # Call the service layer to do the work
    cart_or_error = await CartService.add_item(user_id, item_in)
    
    # Handle the service layer's response
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

    # Success! Manually build the response
    return CartOut(
        id=str(cart_or_error.id),
        user_id=cart_or_error.user_id,
        items=cart_or_error.items
    )

@router.get("/", response_model=CartOut)
async def get_user_cart(
    current_user: User = Depends(get_current_user)
):
    """
    Get the current user's shopping cart.
    """
    cart = await CartService.get_or_create_cart(current_user.id)
    
    return CartOut(
        id=str(cart.id),
        user_id=cart.user_id,
        items=cart.items
    )

@router.delete("/items/{product_id}", response_model=CartOut)
async def remove_item_from_cart(
    product_id: PydanticObjectId,
    current_user: User = Depends(get_current_user)
):
    """
    Remove a product from the current user's shopping cart.
    """
    user_id = current_user.id
    
    cart = await CartService.remove_item(user_id, product_id)
    
    if cart is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found in cart"
        )

    return CartOut(
        id=str(cart.id),
        user_id=cart.user_id,
        items=cart.items
    )