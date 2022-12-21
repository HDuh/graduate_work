from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from src.schemas.product import ProductList, ProductCreate, ProductDetail
from src.services.product import ProductService, get_product_service

router = APIRouter()


@router.get("",
            summary='Get list of products',
            response_model=list[ProductList],
            status_code=HTTPStatus.OK)
async def get_all_products(
        product_service: ProductService = Depends(get_product_service)
) -> list[ProductList]:
    """
        ## Get list of products with the information below:
        - _id_
        - _name_
        - _price_
        - _currency_code_
        - _duration_
    """
    all_products = await product_service.get_all()

    return [ProductList(**product.to_dict()) for product in all_products]


@router.post("",
             summary='Create product',
             response_model=ProductCreate,
             status_code=HTTPStatus.CREATED)
async def create_product(
        product_schema: ProductCreate,
        product_service: ProductService = Depends(get_product_service)
) -> ProductCreate:
    """
        ## Create Product
        Save to DB and send info to Stripe

    """
    result = await product_service.create_product(**product_schema.dict())
    result = ProductCreate(**result.to_dict())
    return result


@router.get("/{product_id}",
            summary='Details product info',
            response_model=ProductDetail,
            status_code=HTTPStatus.OK)
async def get_product_details(
        product_id: UUID,
        product_service: ProductService = Depends(get_product_service)
) -> ProductDetail:
    """
    ## Get details information about product by ID the information below:
    - _id_
    - _name_
    - _description_
    - _duration_
    - _price_
    - _currency_code_
    - _recurring_

    URL params:
    - **{product_id}**
    """
    product = await product_service.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return ProductDetail(**product.to_dict())


@router.delete("/{product_id}",
               summary='Delete product',
               status_code=HTTPStatus.OK)
async def delete_product(
        product_id: UUID,
        product_service: ProductService = Depends(get_product_service)
) -> dict:
    """
     ## Delete Product
        Delete from DB and send info to Stripe

    """
    result = await product_service.remove(product_id)

    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return {'result': f'{product_id} was deleted'}
