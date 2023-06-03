################################################################################
##      Importing necessary modules
################################################################################
import decimal as dec
from fastapi import APIRouter
from fastapi_chameleon import template
from common.viewmodel import ViewModel
from config_settings import conf
from services import (
    item_service as iserv,
    user_service as userv,
    settings_service as setserv,
)


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
    
def adPost_viewmodel():
        return ViewModel(
        error = None
    )


################################################################################
##      Define a route for the adPostListing page
################################################################################

@router.get('/adPostListing')
@template()
async def adPostListing():
    return adPostListing_viewmodel()
    
def adPostListing_viewmodel():
        return ViewModel(
        error = None
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
        )
    return ViewModel(
        error = True,
        error_msg = f'Anúncio {item_id} não encontrado!',
    )