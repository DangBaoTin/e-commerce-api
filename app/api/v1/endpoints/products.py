# app/api/v1/endpoints/products.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.models import Product, User
from app.schemas import ProductCreate, ProductOut
from app.security import get_current_admin_user
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