################################################################################
##      Importing necessary modules
################################################################################
import decimal as dec
from fastapi import APIRouter, Request
from fastapi_chameleon import template
from common.auth import get_current_user
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
@template(template_file='adPost/adPost.html')
async def search(request: Request):
    keyword = request.query_params.get('keyword')
    category = request.query_params.get('category')
    district = request.query_params.get('location')
    price = request.query_params.get('price')
    vm = await search_viewmodel(keyword, category, district, price)

    return vm
    
    

async def search_viewmodel(keyword: str | None, category: str | None, district: str | None,  price: str | None) -> ViewModel:
    
    user = get_current_user()
    if user is None:
        favorites = []
    else:
        favorites = userv.get_user_favorites_ids(user.user_id)
    vm = ViewModel(
        search=iserv.search_item(keyword, category, district, price),
        selected_menu = 'ads',
        categories_images_url = conf('CATEGORIES_IMAGES_URL'),
        districts_images_url = conf('DISTRICTS_IMAGES_URL'),
        items_images_url = conf('ITEMS_IMAGES_URL'),
        num_categories = setserv.count_accepted_categories(),
        num_items = iserv.item_count(),
        location_district = setserv.get_accepted_district(),
        list_category = setserv.get_accepted_category(),
        items_in_category = setserv.count_items_in_categories(),
        latest_items = '',
        user = user,
        favorites = favorites,
    )

    if keyword is None or keyword == '' and category is None and district is None and price is None:
        vm.latest_items = iserv.get_latest_items(LATEST_ITEMS_COUNT)
    elif vm.search == []:
        vm.error, vm.error_msg = True, 'Não foram encontrados anúncios para a pesquisa!'
    else:
        vm.error, vm.error_msg = False, ''    
        
    vm.error = bool(vm.error_msg)

    return vm




################################################################################
##      Define a route for the postDetails page
################################################################################

@router.get('/{item_id}')
@template(template_file='adPost/adPostDetails.html')
async def adPostDetails(item_id: int):
    return adPostDetails_viewmodel(item_id)
    
def adPostDetails_viewmodel(item_id: int) -> ViewModel:
    user = get_current_user()
    if item := iserv.get_item_by_id(item_id):
        return ViewModel(
            selected_menu = 'ads',
            item = item,
            items_images_url = conf('ITEMS_IMAGES_URL'),
            users_images_url = conf('USERS_IMAGES_URL'),
            url_website = conf('URL_WEBSITE'),
            user_created = format_date(userv.get_user_by_id(item.user_id).date_created),
            user = user,
        )
    return ViewModel(
        error = True,
        error_msg = f'Anúncio {item_id} não encontrado!',
    )