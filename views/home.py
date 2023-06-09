################################################################################
##      Importing necessary modules
################################################################################
from fastapi import APIRouter, Request, Response
from fastapi_chameleon import template
from common.auth import get_current_user
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
    user = get_current_user()
    return ViewModel(
        selected_menu = 'home',
        categories_images_url = conf('CATEGORIES_IMAGES_URL'),
        districts_images_url = conf('DISTRICTS_IMAGES_URL'),
        items_images_url = conf('ITEMS_IMAGES_URL'),
        users_images_url = conf('USERS_IMAGES_URL'),
        user = get_current_user(),
        num_items = iserv.item_count(),
        num_users = userv.user_count(),
        num_categories = setserv.count_accepted_categories(),
        num_subcategories = setserv.subcategory_count(),
        location_district = setserv.get_accepted_district(),
        list_category = setserv.get_accepted_category(),
        section_district = setserv.get_random_districts_with_items(SECTION_DISTRICT_COUNT),
        items_in_category = setserv.count_items_in_categories(),
        items_in_district = setserv.count_items_in_districts(),
        popular_items = iserv.most_popular_items(POPULAR_ITEMS_COUNT),
        latest_items = iserv.get_latest_items(LATEST_ITEMS_COUNT),
        random_items = iserv.get_random_items(RANDOM_ITEMS_COUNT),
    )



#################################################################################


@router.get('/search')
@template(template_file='adPost/adPost.html')
async def search(request: Request):
    keyword = request.query_params.get('keyword')
    category = request.query_params.get('category')
    district = request.query_params.get('location')
    vm = await search_viewmodel(keyword, category, district)

    return vm
    
    

async def search_viewmodel(keyword: str | None, category: str | None, district: str | None) -> ViewModel:
    vm = ViewModel(
        selected_menu = 'ads',
        search=iserv.search_item(keyword, category, district),

        categories_images_url = conf('CATEGORIES_IMAGES_URL'),
        districts_images_url = conf('DISTRICTS_IMAGES_URL'),
        items_images_url = conf('ITEMS_IMAGES_URL'),
        num_categories = setserv.count_accepted_categories(),
        num_items = iserv.item_count(),
        location_district = setserv.get_accepted_district(),
        list_category = setserv.get_accepted_category(),
        items_in_category = setserv.count_items_in_categories(),
        latest_items = '',
    )

    if keyword is None or keyword == '' and category is None and district is None:
        vm.latest_items = iserv.get_latest_items(LATEST_ITEMS_COUNT)
    elif vm.search == []:
        vm.error, vm.error_msg = True, 'Não foram encontrados anúncios para a pesquisa!'
    else:
        vm.error, vm.error_msg = False, ''    
        
    vm.error = bool(vm.error_msg)

    return vm


################################################################################
##      Define a route for the howWorks page
################################################################################

@router.get('/howWorks')
@template()
async def howWorks():
    return howWorks_viewmodel()
    
def howWorks_viewmodel():
    return ViewModel(
        selected_menu = 'pages',
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
        selected_menu = 'pages',
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
        selected_menu = 'pages',
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
        selected_menu = 'pages',
        error = None,
    )