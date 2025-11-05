from typing import List
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.repositories.product_repository import product_repository, ProductRepository
from beanie import PydanticObjectId

class ProductService:
    def __init__(self, product_repo: ProductRepository = product_repository):
        self.product_repo = product_repo

    async def get_by_id(self, product_id: PydanticObjectId) -> Product | None:
        """
        Get a product by ID
        """
        return await self.product_repo.get(product_id)

    async def get_all(self) -> List[Product]:
        """
        Get all products
        """
        return await self.product_repo.get_all()

    async def create(self, product_in: ProductCreate) -> Product:
        """
        Create a new product
        """
        return await self.product_repo.create(product_in)

    async def update(
        self, 
        product_id: PydanticObjectId, 
        product_in: ProductUpdate
    ) -> Product | None:
        """
        Update a product
        """
        product = await self.product_repo.get(product_id)
        if not product:
            return None
        
        return await self.product_repo.update(product, product_in)

    async def delete(self, product_id: PydanticObjectId) -> bool:
        """
        Delete a product
        """
        product = await self.product_repo.get(product_id)
        if not product:
            return False
            
        await self.product_repo.delete(product)
        return True

product_service = ProductService()