# Import necessary modules and functions
from fastapi import APIRouter
from fastapi_chameleon import template


router = APIRouter()


@router.get('/viewAds/viewAdsGrid')
async def viewAdsGrid():
    return {
    }



@router.get('/viewAds/viewAdsListing')
async def viewAdsListing():
    return {
    }



@router.get('/viewAds/viewAdsDetails')
async def viewAdsDetails():
    return {
    }