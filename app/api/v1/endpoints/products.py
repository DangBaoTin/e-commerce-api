# app/api/v1/endpoints/products.py
from fastapi import APIRouter, Depends, HTTPException, status

from app.models import Product, User
from app.schemas import ProductCreate, ProductOut, ProductUpdate

from app.api.dependencies import get_current_admin_user
from app.repositories.product_repository import product_repository

from beanie import PydanticObjectId
from beanie.exceptions import DocumentNotFound

router = APIRouter()

@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_in: ProductCreate,
    admin_user: User = Depends(get_current_admin_user)
):
    """
    Create a new product. (Admin only)
    """
    product = await product_repository.create(product_in)
    
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
    Get a list of all available products. (Public)
    """
    products = await product_repository.get_all()
    
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
    Get a single product by its ID. (Public)
    """
    product = await product_repository.get(id)
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
    admin_user: User = Depends(get_current_admin_user)
):
    """
    Update a product's details. (Admin only)
    """
    product = await product_repository.get(id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
        
    updated_product = await product_repository.update(product, product_in)
    
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
    admin_user: User = Depends(get_current_admin_user)
):
    """
    Delete a product. (Admin only)
    """
    product = await product_repository.get(id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
        
    await product_repository.delete(product)
    return None