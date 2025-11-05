from fastapi import APIRouter, Depends, HTTPException, status

from app.models.user import User
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate

from app.api.dependencies import get_current_admin_user

from beanie import PydanticObjectId
from app.services.product_service import product_service

router = APIRouter()

@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_in: ProductCreate,
    _: User = Depends(get_current_admin_user)
):
    """
    Create a new product (Admin only)
    """
    product = await product_service.create(product_in)
    return ProductOut(
        id=str(product.id),
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock
    )

@router.get("/", response_model=list[ProductOut])
async def get_all_products():
    """
    Get list of all products (Public)
    """
    products = await product_service.get_all()
    return [
        ProductOut(
            id=str(p.id),
            name=p.name,
            description=p.description,
            price=p.price,
            stock=p.stock
        ) for p in products
    ]

@router.get("/{id}", response_model=ProductOut)
async def get_product_by_id(id: PydanticObjectId):
    """
    Get  product by ID (Public)
    """
    product = await product_service.get_by_id(id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
        
    return ProductOut(
        id=str(product.id),
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock
    )

@router.put("/{id}", response_model=ProductOut)
async def update_product(
    id: PydanticObjectId,
    product_in: ProductUpdate,
    _: User = Depends(get_current_admin_user)
):
    """
    Update product details (Admin only)
    """
    updated_product = await product_service.update(id, product_in)
    
    if not updated_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    
    return ProductOut(
        id=str(updated_product.id),
        name=updated_product.name,
        description=updated_product.description,
        price=updated_product.price,
        stock=updated_product.stock
    )

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    id: PydanticObjectId,
    _: User = Depends(get_current_admin_user)
):
    """
    Delete a product (Admin only)
    """
    success = await product_service.delete(id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
        
    return None