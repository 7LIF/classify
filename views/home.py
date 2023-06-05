################################################################################
##      Importing necessary modules
################################################################################
from typing import Optional
from unicodedata import category
from fastapi import APIRouter, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi_chameleon import template
from common.viewmodel import ViewModel
from config_settings import conf
from services import (
    item_service as iserv,
    user_service as userv,
    settings_service as setserv,
)

from common.auth import get_session

################################################################################
##      Constants
################################################################################

LIST_CATEGORY_COUNT = 11
LATEST_ITEMS_COUNT = 8
POPULAR_ITEMS_COUNT = 8
RANDOM_ITEMS_COUNT = 8
LOCATION_DISTRICT_COUNT = 21
SECTION_DISTRICT_COUNT = 3


################################################################################
##      Create an instance of the router
################################################################################

router = APIRouter()


################################################################################
##      Define a route for the index/home page
################################################################################

@router.get('/')
@template()
async def index():
    return index_viewmodel()

def index_viewmodel() -> ViewModel:
    return ViewModel(
        categories_images_url = conf('CATEGORIES_IMAGES_URL'),
        districts_images_url = conf('DISTRICTS_IMAGES_URL'),
        items_images_url = conf('ITEMS_IMAGES_URL'),
        users_images_url = conf('USERS_IMAGES_URL'),
        num_items = iserv.item_count(),
        num_users = userv.user_count(),
        num_categories = setserv.count_accepted_categories(),
        num_subcategories = setserv.subcategory_count(),
        location_district = setserv.get_accepted_district(),
        list_category = setserv.get_accepted_category(),
        section_district = setserv.get_random_districts_with_items(SECTION_DISTRICT_COUNT),
        items_in_category = setserv.count_items_in_categories(),
        popular_items = iserv.most_popular_items(POPULAR_ITEMS_COUNT),
        latest_items = iserv.get_latest_items(LATEST_ITEMS_COUNT),
        random_items = iserv.get_random_items(RANDOM_ITEMS_COUNT),
    )



#################################################################################

@router.get('/search')
@template(template_file='adPost/adPost.html')
async def search(request: Request):
    keyword = request.query_params.get('keyword')
    if keyword is not None:
        viewmodel = search_viewmodel(keyword)
        if viewmodel['keyword'] is not None:
            return viewmodel  # Retorna a viewmodel diretamente
        else:
            return Response(content="Nenhum resultado encontrado", status_code=200)
    else:
        return Response(content="Palavra-chave não encontrada", status_code=400)


def search_viewmodel(keyword: str | None) -> ViewModel:
    return ViewModel(
        keyword=iserv.search_item(keyword),
        
        categories_images_url = conf('CATEGORIES_IMAGES_URL'),
        districts_images_url = conf('DISTRICTS_IMAGES_URL'),
        items_images_url = conf('ITEMS_IMAGES_URL'),
        num_categories = setserv.count_accepted_categories(),
        num_items = iserv.item_count(),
        location_district = setserv.get_accepted_district(),
        list_category = setserv.get_accepted_category(),
        items_in_category = setserv.count_items_in_categories(),
        latest_items = iserv.get_latest_items(LATEST_ITEMS_COUNT),
        random_items = iserv.get_random_items(RANDOM_ITEMS_COUNT),
    )







################################################################################
##      Define a route for the howWorks page
################################################################################

@router.get('/howWorks')
@template()
async def howWorks():
    return howWorks_viewmodel()
    
def howWorks_viewmodel():
        return ViewModel(
        error = None,
    )


################################################################################
##      Define a route for the about page
################################################################################

@router.get('/about')
@template()
async def about():
    return about_viewmodel()
    
def about_viewmodel():
        return ViewModel(
        error = None,
    )



################################################################################
##      Define a route for the contact page
################################################################################

@router.get('/contact')
@template()
async def contact():
    return contact_viewmodel()
    
def contact_viewmodel():
        return ViewModel(
        error = None,
    )



################################################################################
##      Define a route for the faq page
################################################################################

@router.get('/faq')
@template()
async def faq():
    return faq_viewmodel()
    
def faq_viewmodel():
        return ViewModel(
        error = None,
    )