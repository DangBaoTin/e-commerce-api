# app/repositories/product_repository.py
from typing import List
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from beanie import PydanticObjectId

class ProductRepository:
    """
    This class handles all database operations for the Product model.
    """
    
    async def get(self, product_id: PydanticObjectId) -> Product | None:
        """
        Get a single product by its ID.
        """
        return await Product.get(product_id)

    async def get_all(self) -> List[Product]:
        """
        Get a list of all products.
        """
        return await Product.find_all().to_list()

    async def create(self, product_in: ProductCreate) -> Product:
        """
        Create a new product.
        """
        product = Product(**product_in.model_dump())
        await product.insert()
        return product

    async def update(
        self, 
        product: Product, 
        product_in: ProductUpdate
    ) -> Product:
        """
        Update a product (given the product document and update data).
        """
        update_data = product_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(product, key, value)
        await product.save()
        return product

    async def delete(self, product: Product) -> None:
        """
        Delete a product (given the product document).
        """
        await product.delete()

    async def save(self, product: Product) -> Product:
        """
        Saves a product document. Used for stock updates.
        """
        await product.save()
        return product

# Create a single instance
product_repository = ProductRepository()