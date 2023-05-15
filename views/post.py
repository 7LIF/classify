# Import necessary modules and functions
from fastapi import APIRouter, Request
from fastapi_chameleon import template
from common.viewmodel import ViewModel
from fastapi_chameleon import template


router = APIRouter()


@router.get('/post')
@template()
async def post():
    return post_viewmodel()
    
def post_viewmodel():
        return ViewModel(
        error = None,
        # 'error_msg': 'There was an error with your data. Please try again.'
    )



@router.get('/post/postListing')
@template()
async def postListing():
    return postListing_viewmodel()
    
def postListing_viewmodel():
        return ViewModel(
        error = None,
        # 'error_msg': 'There was an error with your data. Please try again.'
    )



@router.get('/post/postDetails')
@template()
async def postDetails():
    return postDetails_viewmodel()
    
def postDetails_viewmodel():
        return ViewModel(
        error = None,
        # 'error_msg': 'There was an error with your data. Please try again.'
    )