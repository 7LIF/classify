################################################################################
##      Importing necessary modules
################################################################################

from datetime import date
from fastapi import APIRouter, Request, Response, Depends, responses, status
from fastapi_chameleon import template
from common.auth import set_auth_cookie, delete_auth_cookie
from common.common import MIN_DATE, is_valid_name, is_valid_email, is_valid_password, is_valid_iso_date
from common.fastapi_utils import form_field_as_str
from common.viewmodel import ViewModel
from services import user_service, category_service, location_service
from services.user_service import authenticate_user_by_email



################################################################################
##      Constants
################################################################################

LIST_CATEGORY_COUNT = 11
LOCATION_DISTRICT_COUNT = 21


################################################################################
##      Create an instance of the router
################################################################################

router = APIRouter()


################################################################################
##      Define a route for the account page
################################################################################

@router.get('/account')
@template()
async def account():
    return account_viewmodel()
    
def account_viewmodel():
        return ViewModel(
        error = None,
        # 'error_msg': 'There was an error with your data. Please try again.'
    )



################################################################################
##      Define a route and View model for the register page
################################################################################

@router.get('/account/register')
@template()
async def register():
    return register_viewmodel()


def register_viewmodel():
    return ViewModel(
        name = '',
        email_addr ='',
        password = '',
        checked = False,
    )


################################################################################
##     Handling the POST request and view model for registration
################################################################################

@router.post('/account/register')
@template(template_file='account/register.html')
async def post_register(request: Request):
    vm = await post_register_viewmodel(request)

    if vm.error:
        return vm
    
    response = responses.RedirectResponse(url='/', status_code = status.HTTP_302_FOUND)
    set_auth_cookie(response, vm.new_user_id)
    return response

    
    
async def post_register_viewmodel(request: Request):
    form_data = await request.form()
    vm = ViewModel(
        name = form_field_as_str(form_data, 'name'),
        email_addr = form_field_as_str(form_data, 'email_addr'),
        password = form_field_as_str(form_data, 'password'),
        new_user_id = None
    )

    if not is_valid_name(vm.name):
        vm.error, vm.error_msg = True, 'Nome inválido!'
    elif not is_valid_email(vm.email_addr):
        vm.error, vm.error_msg = True, 'Endereço de email inválido!'
    elif not is_valid_password(vm.password):
        vm.error, vm.error_msg = True, 'Palavra-passe inválida!'
    elif user_service.get_user_by_email(vm.email_addr):
        vm.error, vm.error_msg = True, f'O endereço de email {vm.email_addr} já está registado!'
    else:
        vm.error, vm.error_msg = False, ''

    if not vm.error:
        user = user_service.create_account(
            vm.name,
            vm.email_addr,
            vm.password,
        )
        vm.new_user_id = user.id

    return vm


################################################################################
##      Define a route and View model for the login page
################################################################################

@router.get('/account/login')
@template()
async def login():
    return login_viewmodel()
    
def login_viewmodel():
    return ViewModel(
        email_addr = '',
        password = '',  
    )
    

################################################################################
##     Handling the POST request and view model for login
################################################################################

@router.post('/account/login')
@template(template_file='account/login.html')
async def post_login(request: Request):
    vm = await post_login_viewmodel(request)

    if vm.error:
        return vm
    
    response = responses.RedirectResponse(url='/', status_code = status.HTTP_302_FOUND)
    set_auth_cookie(response, vm.user_id)
    return response


async def post_login_viewmodel(request: Request) -> ViewModel:
    form_data = await request.form()
    vm = ViewModel(
        email_addr = form_field_as_str(form_data, 'email_addr'),
        password = form_field_as_str(form_data, 'password'),
        user_id = None,
    )

    if not is_valid_email(vm.email_addr):
        vm.error, vm.error_msg = True, 'Inválido utilizador ou palavra-passe!'
    elif not is_valid_password(vm.password):
        vm.error, vm.error_msg = True, 'Palavra-passe inválida!'
    elif not (user := user_service.authenticate_user_by_email(vm.email_addr, vm.password)):
        vm.error, vm.error_msg = True, 'Utilizador não encontrado!'
    else:
        vm.error, vm.error_msg = False, ''
        vm.user_id = user.id

    return vm

  
################################################################################
##      Define a route and View model for the logout page
################################################################################

@router.get('/account/logout')
async def logout():
    response = responses.RedirectResponse(url='/', status_code = status.HTTP_302_FOUND)
    delete_auth_cookie(response)
    return response



################################################################################
##      Define a route and View model for the dashboard page and all pages submenus
################################################################################
    
@router.get('/account/profileSettings')
@template()
async def profileSettings():
    return profileSettings_viewmodel()
    
def profileSettings_viewmodel():
        return ViewModel(
        error = None,
        # 'error_msg': 'There was an error with your data. Please try again.'
    )


@router.get('/account/myAds')
@template()
async def myAds():
    return myAds_viewmodel()
    
def myAds_viewmodel():
        return ViewModel(
        error = None,
        # 'error_msg': 'There was an error with your data. Please try again.'
    )
    
    
    
@router.get('/account/favoritesAds')
@template()
async def favoritesAds():
    return favoritesAds_viewmodel()
    
def favoritesAds_viewmodel():
        return ViewModel(
        error = None,
        # 'error_msg': 'There was an error with your data. Please try again.'
    )
    
    
    
@router.get('/account/postAd')
@template()
async def postAd():
    return postAd_viewmodel()
    
def postAd_viewmodel():
    return ViewModel(
        list_category = category_service.list_category(LIST_CATEGORY_COUNT),
        location_district = location_service.location_district(LOCATION_DISTRICT_COUNT)
    )
    
    
    
@router.get('/account/messages')
@template()
async def messages():
    return messages_viewmodel()
    
def messages_viewmodel():
        return ViewModel(
        error = None,
        # 'error_msg': 'There was an error with your data. Please try again.'
    )
    
    
    
@router.get('/account/deleteAccount')
@template()
async def deleteAccount():
    return deleteAccount_viewmodel()
    
def deleteAccount_viewmodel():
        return ViewModel(
        error = None,
        # 'error_msg': 'There was an error with your data. Please try again.'
    )

        
        
@router.get('/account/mailSuccess')
@template()
async def mailSuccess():
    return mailSuccess_viewmodel()
    
def mailSuccess_viewmodel():
        return ViewModel(
        error = None,
        # 'error_msg': 'There was an error with your data. Please try again.'
    )