from http import HTTPStatus
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from src.schemas.product import ProductList, ProductCreate, ProductDetail
from src.services.product import ProductService, get_product_service

router = APIRouter()


@router.get("",
            response_model=list[ProductList],
            status_code=HTTPStatus.OK)
async def get_all_products(
        product_service: ProductService = Depends(get_product_service)
) -> List[ProductList]:
    all_products = await product_service.get_all()

    return [ProductList(**product.to_dict()) for product in all_products]


@router.post("",
             response_model=ProductCreate,
             status_code=HTTPStatus.CREATED)
async def create_product(
        product_schema: ProductCreate,
        product_service: ProductService = Depends(get_product_service)
) -> ProductCreate:
    result = await product_service.create_product(**product_schema.dict())
    result = ProductCreate(**result.to_dict())
    return result


@router.get("/{product_id}",
            response_model=ProductDetail,
            status_code=HTTPStatus.OK)
async def get_product_details(
        product_id: UUID,
        product_service: ProductService = Depends(get_product_service)
) -> ProductDetail:
    product = await product_service.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return ProductDetail(**product.to_dict())


@router.delete("/{product_id}",
               status_code=HTTPStatus.OK)
async def delete_product(
        product_id: UUID,
        product_service: ProductService = Depends(get_product_service)
) -> dict:
    result = await product_service.remove(product_id)

    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return {'result': f'{product_id} was deleted'}
