# Import necessary modules and functions
from fastapi import APIRouter
from fastapi_chameleon import template


router = APIRouter()


@router.get('/post/postGrid')
async def postGrid():
    return {
    }



@router.get('/post/postListing')
async def postListing():
    return {
    }



@router.get('/post/postDetails')
async def postDetails():
    return {
    }