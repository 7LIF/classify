################################################################################
##      Importing necessary modules
################################################################################

from fastapi import APIRouter
from fastapi_chameleon import template
from common.viewmodel import ViewModel



################################################################################
##      Create an instance of the router
################################################################################

router = APIRouter()



################################################################################
##      Define a route for the error404 page
################################################################################

@router.get('/error404')
@template(template_file='errors/error404.html')
async def error404():
    return error404_viewmodel()
    
def error404_viewmodel():
        return ViewModel(
        error = None
    )
