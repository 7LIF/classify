# Import necessary modules and functions
from fastapi import APIRouter
from fastapi_chameleon import template
from common.viewmodel import ViewModel

router = APIRouter()


@router.get('/error404')
@template()
async def error404():
    return error404_viewmodel()
    
def error404_viewmodel():
        return ViewModel(
        error = None,
        # 'error_msg': 'There was an error with your data. Please try again.'
    )
