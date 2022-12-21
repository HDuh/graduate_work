from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter
from starlette.responses import JSONResponse

from src.core import ActivationChoice
from src.db.models import Product
from src.schemas import ProductCreateSchema, ProductResponseSchema, MessageResponse
from src.services import DbManager, StripeManager

router = APIRouter()


@router.get(
    "/all_products",
    response_model=list[ProductResponseSchema],
    status_code=HTTPStatus.OK,
    summary='Получить список всех продуктов'
)
async def get_all_products() -> list[ProductResponseSchema]:
    """
        ## Получить список всех продуктов
    """
    all_products = await DbManager.async_get_all(Product)
    return [ProductResponseSchema(**product.to_dict()) for product in all_products]


@router.post(
    "/create_product",
    responses={
        200: {'model': ProductResponseSchema},
        409: {'model': MessageResponse},
    },
    summary='Создать новый продукт'
)
async def create_product(product_schema: ProductCreateSchema) -> ProductResponseSchema | JSONResponse:
    """
        ## Создать новый продукт:
        _product_schema_ - модель продукта
    """
    if await DbManager.async_get_by_name(Product, product_schema.name):
        return JSONResponse(
            status_code=HTTPStatus.CONFLICT,
            content={'message': f'Product {product_schema.name} already exist in database'}
        )

    if product_schema.recurring:
        product_schema.recurring_params = {
            "aggregate_usage": None,
            "interval": "month",
            "interval_count": product_schema.duration,
            "usage_type": "licensed"
        }

    product_schema.product_stripe_id = StripeManager.create_product(product_schema).stripe_id
    product_schema.price_stripe_id = StripeManager.create_price(product_schema).stripe_id
    product_instance = Product(**product_schema.to_dict())
    await DbManager.async_save(product_instance)
    return ProductResponseSchema(**product_instance.to_dict())


@router.get(
    "/product_info/{product_id}",
    responses={
        200: {'model': ProductResponseSchema},
        404: {'model': MessageResponse},
    },
    summary='Получить информацию о конкретном продукте'
)
async def get_product_details(product_id: UUID) -> ProductResponseSchema | JSONResponse:
    """
        ## Получить информацию о конкретном продукте:
        _product_id_ - идентификатор продукта
    """
    if not (product := await DbManager.async_get_by_id(Product, product_id)):
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content={'message': f'Product {product_id} not found in database'}
        )
    return ProductResponseSchema(**product.to_dict())


@router.delete(
    "/delete_product/{product_id}",
    responses={
        200: {'model': MessageResponse},
        404: {'model': MessageResponse},
    },
    summary='Удалить конкретный продукт'
)
async def delete_product(product_id: UUID) -> JSONResponse:
    """
        ## Удалить конкретный продукт:
        _product_id_ - идентификатор продукта
    """
    if not (product := await DbManager.async_get_by_id(Product, product_id)):
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content={'message': f'Product {product_id} not found in database'}
        )
    StripeManager.archive_product(product)
    await DbManager.async_delete(product)
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={'message': f'Product {product_id} delete successfully'}
    )


@router.put(
    "/update_product_status/{product_id}",
    responses={
        200: {'model': MessageResponse},
        404: {'model': MessageResponse},
    },
    summary='Изменить статус продукта'
)
async def change_product_status(product_id: UUID, status: ActivationChoice) -> JSONResponse:
    """
        ## Изменить статус конкретного продукта:
        _product_id_ - идентификатор продукта
        _status_ - присваиваемый статус
    """
    is_active = True if status == ActivationChoice.ACTIVE else False
    if not (product := await DbManager.async_get_by_id(Product, product_id)):
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content={'message': f'Product {product_id} not found in database'}
        )
    StripeManager.archive_product(product, is_active)
    await DbManager.async_update(product, is_active=is_active)
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={'message': f'Product {product_id} set status {status.value.upper()} successfully'}
    )
