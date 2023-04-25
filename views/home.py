# Import necessary modules and functions
from fastapi import APIRouter
from fastapi_chameleon import template


router = APIRouter()


@router.get('/')
@template()
async def index(course1: str = 'N/D'):
    return {
        'course1': course1,
        'course2': 'Biogenética Aplicada',
        'course3': 'Pesca de Grande Porte',
    }

@router.get('/howWorks')
@template()
async def howWorks():
    return {
    }


@router.get('/pricing')
@template()
async def pricing():
    return {
    }



@router.get('/aboutUs')
@template()
async def aboutUs():
    return {
    }



@router.get('/contactUs')
@template()
async def contactUs():
    return {
    }


@router.get('/faq')
@template()
async def faq():
    return {
    }