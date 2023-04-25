# Import necessary modules and functions
from fastapi import APIRouter
from fastapi_chameleon import template


router = APIRouter()


@router.get('/account/register')
async def register():
    return {
    }


@router.get('/account/login')
async def login():
    return {
    }


@router.get('/account/dashboard')
async def dashboard():
    return {
    }


@router.get('/account/profileSettings')
async def profileSettings():
    return {
    }


@router.get('/account/myAds')
async def myAds():
    return {
    }


@router.get('/account/favoritesAds')
async def favoritesAds():
    return {
    }


@router.get('/account/postAd')
async def postAd():
    return {
    }


@router.get('/account/bookmarkedAds')
async def bookmarkedAds():
    return {
    }


@router.get('/account/messages')
async def messages():
    return {
    }


@router.get('/account/invoce')
async def invoce():
    return {
    }


@router.get('/account/deleteAccount')
async def deleteAccount():
    return {
    }