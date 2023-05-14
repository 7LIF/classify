# Import necessary modules and functions
from fastapi import APIRouter, Request
from starlette.requests import Request
from fastapi_chameleon import template
from common.viewmodel import base_viewmodel_with
from services import category_service, location_service, item_service, user_service


router = APIRouter()


LIST_CATEGORY_COUNT = 11
LATEST_ITEMS_COUNT = 8
POPULAR_ITEMS_COUNT = 8
RANDOM_ITEMS_COUNT = 8
LOCATION_DISTRICT_COUNT = 21


@router.get('/')
@template()
async def index(response: Request):
    return index_viewmodel()


def index_viewmodel():
    return base_viewmodel_with({
        'list_category': category_service.list_category(LIST_CATEGORY_COUNT),
        'location_district': location_service.location_district(LOCATION_DISTRICT_COUNT),
        'latest_items': item_service.latest_items(LATEST_ITEMS_COUNT),
        'popular_items': item_service.popular_items(POPULAR_ITEMS_COUNT),
        'random_items': item_service.random_items(RANDOM_ITEMS_COUNT),
    })


@router.get('/howWorks')
@template()
async def howWorks():
    return {
    }


@router.get('/pricing')
@template()
async def pricing():
    return {
    }



@router.get('/aboutUs')
@template()
async def aboutUs():
    return {
    }



@router.get('/contactUs')
@template()
async def contactUs():
    return {
    }


@router.get('/faq')
@template()
async def faq():
    return {
    }