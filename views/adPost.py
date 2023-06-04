################################################################################
##      Importing necessary modules
################################################################################
import decimal as dec
from fastapi import APIRouter, Request
from fastapi_chameleon import template
from common.common import format_date
from common.viewmodel import ViewModel
from config_settings import conf
from services import (
    item_service as iserv,
    user_service as userv,
    settings_service as setserv,
)


################################################################################
##      Constants
################################################################################

LATEST_ITEMS_COUNT = 10
RANDOM_ITEMS_COUNT = 10

################################################################################
##      SETUP FastAPI - Create an instance of the router
################################################################################

router = APIRouter(prefix = '/adPost')



################################################################################
##      Define a route for the post page
################################################################################

@router.get('/')
@template()
async def adPost():
    return adPost_viewmodel()
    
def adPost_viewmodel() -> ViewModel:
        return ViewModel(
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
##      Define a route for the postDetails page
################################################################################

@router.get('/{item_id}')
@template(template_file='adPost/adPostDetails.html')
async def adPostDetails(item_id: int):
    return adPostDetails_viewmodel(item_id)
    
def adPostDetails_viewmodel(item_id: int) -> ViewModel:
    if item := iserv.get_item_by_id(item_id):
        return ViewModel(
            item = item,
            items_images_url = conf('ITEMS_IMAGES_URL'),
            users_images_url = conf('USERS_IMAGES_URL'),
            url_website = conf('URL_WEBSITE'),
            user_created = format_date(userv.get_user_by_id(item.user_id).date_created)
        )
    return ViewModel(
        error = True,
        error_msg = f'Anúncio {item_id} não encontrado!',
    )