################################################################################
##      Importing necessary modules
################################################################################
from unicodedata import category
from fastapi import APIRouter, Request, Response, Depends, responses, status
from fastapi_chameleon import template
from starlette.responses import RedirectResponse as RedirectResponse
from common.common import coalesce
from common.fastapi_utils import form_field_as_str
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
   



@router.post('/')
@template()
async def index_search(request: Request):
    vm = await index_viewmodel(request)
    
    if vm.error:
        return vm
    
    items = await iserv.search_items(vm.keyword, vm.category, vm.location)
    vm.items = items
    
    return vm

@router.post('/redirect')
async def redirect():
    return RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)




async def index_viewmodel(request: Request = None) -> ViewModel:
    vm = ViewModel(
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
    
    if request and request.method == 'POST':
        form_data = await request.form()
        vm.keyword = form_field_as_str(form_data, 'keyword').strip()
        vm.category = form_field_as_str(form_data, 'category').strip()
        vm.location = form_field_as_str(form_data, 'location').strip()
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