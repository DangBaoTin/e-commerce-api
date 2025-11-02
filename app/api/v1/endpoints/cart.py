# app/api/v1/endpoints/cart.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.models import Product, User, Cart, CartItem
from app.schemas import CartItemCreate, CartOut
from app.security import get_current_user
from beanie import PydanticObjectId

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
    # 1. Check if product exists and has enough stock
    product = await Product.get(item_in.product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    if product.stock < item_in.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough stock"
        )

    # 2. Get or create the user's cart
    cart = await get_or_create_cart(current_user.id) # type: ignore

    # 3. Check if item is already in cart
    existing_item = None
    for item in cart.items:
        if item.product_id == item_in.product_id:
            existing_item = item
            break

    # 4. Update cart logic
    if existing_item:
        # Check new total quantity against stock
        new_quantity = existing_item.quantity + item_in.quantity
        if product.stock < new_quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Not enough stock. Only {product.stock} available."
            )
        existing_item.quantity = new_quantity
    else:
        # Item not in cart, add it
        cart.items.append(CartItem(**item_in.model_dump()))

    # 5. Save the cart and return it
    await cart.save()
    
    return CartOut(
        id=str(cart.id),
        user_id=cart.user_id,
        items=cart.items
    )

@router.get("/", response_model=CartOut)
async def get_user_cart(
    current_user: User = Depends(get_current_user)
):
    """
    Get the current user's shopping cart.
    """
    cart = await get_or_create_cart(current_user.id) # type: ignore
    
    return CartOut(
        id=str(cart.id),
        user_id=cart.user_id,
        items=cart.items
    )