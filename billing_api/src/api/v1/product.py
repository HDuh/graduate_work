from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends

from schemas.product import ProductList, ProductCreate
from services.product import ProductService, get_product_service

router = APIRouter()


@router.get("/",
            response_model=List[ProductList],
            status_code=HTTPStatus.OK)
async def get_all_products(
        product_service: ProductService = Depends(get_product_service)
) -> List[ProductList]:
    return await product_service.get_all()


@router.post("/",
             response_model=ProductCreate,
             status_code=HTTPStatus.OK)
async def create_product(
        product_schema: ProductCreate,
        product_service: ProductService = Depends(get_product_service)
) -> dict:
    result = await product_service.create_product(**product_schema.dict())
    return result
