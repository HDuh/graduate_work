from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from source.schemas.product import ProductList, ProductCreate, ProductDetail
from source.services.product import ProductService, get_product_service

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
             status_code=HTTPStatus.CREATED)
async def create_product(
        product_schema: ProductCreate,
        product_service: ProductService = Depends(get_product_service)
) -> ProductCreate:
    result = await product_service.create_product(**product_schema.dict())
    return result


@router.get("/{product_id}",
            response_model=ProductDetail,
            status_code=HTTPStatus.OK)
async def get_product_details(
        product_id: int,
        product_service: ProductService = Depends(get_product_service)
) -> ProductDetail:
    product = await product_service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return product


@router.delete("/{product_id}",
               response_model=dict,
               status_code=HTTPStatus.OK)
async def delete_product(
        product_id: int,
        product_service: ProductService = Depends(get_product_service)
) -> dict:
    result = await product_service.delete_product(product_id)
    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return result
