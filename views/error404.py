# Import necessary modules and functions
from fastapi import APIRouter
from fastapi_chameleon import template


router = APIRouter()


@router.get('/error404')
@template()
async def error404():
    return {
    }
