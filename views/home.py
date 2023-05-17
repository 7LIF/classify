################################################################################
##      Importing necessary modules
################################################################################
from fastapi import APIRouter
from fastapi_chameleon import template
from services import category_service, location_service, item_service
from common.viewmodel import ViewModel



################################################################################
##      Create an instance of the router
################################################################################

router = APIRouter()



################################################################################
##      Constants
################################################################################

LIST_CATEGORY_COUNT = 11
LATEST_ITEMS_COUNT = 8
POPULAR_ITEMS_COUNT = 8
RANDOM_ITEMS_COUNT = 8
LOCATION_DISTRICT_COUNT = 21



################################################################################
##      Define a route for the index/home page
################################################################################

@router.get('/')
@template()
async def index():
    return index_viewmodel()

def index_viewmodel():
    return ViewModel(
        list_category = category_service.list_category(LIST_CATEGORY_COUNT),
        location_district = location_service.location_district(LOCATION_DISTRICT_COUNT),
        latest_items = item_service.latest_items(LATEST_ITEMS_COUNT),
        popular_items = item_service.popular_items(POPULAR_ITEMS_COUNT),
        random_items = item_service.random_items(RANDOM_ITEMS_COUNT)
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
        # 'error_msg': 'There was an error with your data. Please try again.'
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
        # 'error_msg': 'There was an error with your data. Please try again.'
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
        # 'error_msg': 'There was an error with your data. Please try again.'
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
        # 'error_msg': 'There was an error with your data. Please try again.'
    )