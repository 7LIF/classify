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

router = APIRouter(prefix = '/post')



################################################################################
##      Define a route for the post page
################################################################################

@router.get('/')
@template()
async def post():
    return post_viewmodel()
    
def post_viewmodel():
        return ViewModel(
        error = None
    )


################################################################################
##      Define a route for the postDetails page
################################################################################

@router.get('/{item_id}}')
@template()
async def postDetails(item_id: int):
    return postDetails_viewmodel(item_id)
    
def postDetails_viewmodel(item_id: int) -> ViewModel:
    if item := iserv.get_item_by_id(item_id):
        item_price = dec(item.price)
        return ViewModel(
            item = item,
            item_price = f'{item_price} €',
            images_url = conf('IMAGES_URL'),
            users_imagens_url = conf('USERS_IMAGES_URL'),
        )
    return ViewModel(
        error = None,
        error_msg = f'Anúncio {id} não encontrado!',
    )