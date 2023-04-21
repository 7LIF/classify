# Import necessary modules and functions
from fastapi import APIRouter
from fastapi_chameleon import template


router = APIRouter()


@router.get('/account')
async def account():
    return {
    }



@router.get('/account/login')
async def login():
    return {
    }



@router.get('/account/register')
async def register():
    return {
    }