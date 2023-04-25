# Import necessary modules and functions
from fastapi import APIRouter
from fastapi_chameleon import template


router = APIRouter()


@router.get('/viewAds')
async def viewAds():
    return {
    }
