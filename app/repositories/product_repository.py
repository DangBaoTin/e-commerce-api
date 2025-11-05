from typing import List
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from beanie import PydanticObjectId

class ProductRepository:
    async def get(self, product_id: PydanticObjectId) -> Product | None:
        """
        Get single product by ID
        """
        return await Product.get(product_id)

    async def get_all(self) -> List[Product]:
        """
        Get list of all products.
        """
        return await Product.find_all().to_list()

    async def create(self, product_in: ProductCreate) -> Product:
        """
        Create new product.
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
        Update product
        """
        update_data = product_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(product, key, value)
        await product.save()
        return product

    async def delete(self, product: Product) -> None:
        """
        Delete product
        """
        await product.delete()

    async def save(self, product: Product) -> Product:
        """
        Saves product document > used for stock updates
        """
        await product.save()
        return product

# Create a single instance
product_repository = ProductRepository()