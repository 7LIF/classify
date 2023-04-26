# Import necessary modules and functions
from fastapi import APIRouter
from fastapi_chameleon import template


router = APIRouter()


@router.get('/account/register')
@template()
async def register():
    return {
    }


@router.get('/account/login')
@template()
async def login():
    return {
    }


@router.get('/account/dashboard')
@template()
async def dashboard():
    return {
    }


@router.get('/account/profileSettings')
@template()
async def profileSettings():
    return {
    }


@router.get('/account/myAds')
@template()
async def myAds():
    return {
    }


@router.get('/account/favoritesAds')
@template()
async def favoritesAds():
    return {
    }


@router.get('/account/postAd')
@template()
async def postAd():
    return {
    }


@router.get('/account/bookmarkedAds')
@template()
async def bookmarkedAds():
    return {
    }


@router.get('/account/messages')
@template()
async def messages():
    return {
    }


@router.get('/account/invoce')
@template()
async def invoce():
    return {
    }


@router.get('/account/deleteAccount')
@template()
async def deleteAccount():
    return {
    }


@router.get('/account/mailSuccess')
@template()
async def mailSuccess():
    return {
    }