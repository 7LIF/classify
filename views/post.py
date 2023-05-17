################################################################################
##      Importing necessary modules
################################################################################
from fastapi import APIRouter
from fastapi_chameleon import template
from common.viewmodel import ViewModel
from services import item_service



################################################################################
##      Create an instance of the router
################################################################################

router = APIRouter()



################################################################################
##      Define a route for the post page
################################################################################

@router.get('/post')
@template()
async def post():
    return post_viewmodel()
    
def post_viewmodel():
        return ViewModel(
        error = None,
        # 'error_msg': 'There was an error with your data. Please try again.'
    )



################################################################################
##      Define a route for the postListing page
################################################################################

@router.get('/post/postListing')
@template()
async def postListing():
    return postListing_viewmodel()
    
def postListing_viewmodel():
        return ViewModel(
        error = None,
        # 'error_msg': 'There was an error with your data. Please try again.'
    )



################################################################################
##      Define a route for the postDetails page
################################################################################

@router.get('/post/{item_id}}')
@template()
async def postDetails(item_id: int):
    return postDetails_viewmodel(item_id)
    
def postDetails_viewmodel(item_id: int):
    if item := item_service.get_item_by_id(item_id):
        return ViewModel(
            item = item
    )
    return ViewModel(
        error = None,
        error_msg = 'Anúncio não encontrado!',
    )