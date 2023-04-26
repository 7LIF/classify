# Import necessary modules and functions
from fastapi import APIRouter
from fastapi_chameleon import template


router = APIRouter()


@router.get('/post/postGrid')
@template()
async def postGrid():
    return {
    }



@router.get('/post/postListing')
@template()
async def postListing():
    return {
    }



@router.get('/post/postDetails')
@template()
async def postDetails():
    return {
    }