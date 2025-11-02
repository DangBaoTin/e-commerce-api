# app/api/v1/endpoints/products.py
from fastapi import APIRouter, Depends, HTTPException, status

from app.models import Product, User
from app.schemas import ProductCreate, ProductOut, ProductUpdate

from app.security import get_current_admin_user
from beanie import PydanticObjectId
from beanie.exceptions import DocumentNotFound

router = APIRouter()

@router.post(
    "/", 
    response_model=ProductOut, 
    status_code=status.HTTP_201_CREATED
)
async def create_product(
    product_in: ProductCreate,
    admin_user: User = Depends(get_current_admin_user)
):
    """
    Create a new product. This endpoint is protected and
    only accessible by administrators.
    """
    product = Product(**product_in.model_dump())
    await product.insert()
    
    # Manually create the ProductOut to include the ID
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
    Get a list of all available products.
    This is a public endpoint.
    """
    products = await Product.find_all().to_list()
    
    # Convert list of Product documents to list of ProductOut schemas
    return [
        ProductOut(
            id=str(p.id),
            name=p.name,
            description=p.description,
            price=p.price,
            stock=p.stock
        ) for p in products
    ]

# --- 1. ADD NEW ENDPOINT: GET ONE PRODUCT ---
@router.get("/{id}", response_model=ProductOut)
async def get_product_by_id(id: PydanticObjectId):
    """
    Get a single product by its ID. (Public)
    """
    try:
        product = await Product.get(id)
    except DocumentNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    
    if not product: # Redundant check, but good practice
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

# --- 2. ADD NEW ENDPOINT: UPDATE PRODUCT ---
@router.put("/{id}", response_model=ProductOut)
async def update_product(
    id: PydanticObjectId,
    product_in: ProductUpdate,
    admin_user: User = Depends(get_current_admin_user)
):
    """
    Update a product's details. (Admin only)
    """
    product = await Product.get(id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
        
    # Get update data, excluding unset fields
    update_data = product_in.model_dump(exclude_unset=True)
    
    # Update the product fields
    for key, value in update_data.items():
        setattr(product, key, value)
        
    await product.save()
    
    return ProductOut(
        id=str(product.id),
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock
    )

# --- 3. ADD NEW ENDPOINT: DELETE PRODUCT ---
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    id: PydanticObjectId,
    admin_user: User = Depends(get_current_admin_user)
):
    """
    Delete a product. (Admin only)
    """
    product = await Product.get(id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
        
    await product.delete()
    
    # Return 204 No Content, which means success, but no body
    return None