################################################################################
##      Importing necessary modules
################################################################################

from datetime import date
from werkzeug.utils import secure_filename
import os
from fastapi import APIRouter, File, HTTPException, Request, Response, Depends, UploadFile, responses, status
from fastapi_chameleon import template
from requests import Session
from common.fastapi_utils import form_field_as_str, form_field_as_file, upload_file_closing
from common.viewmodel import ViewModel
from config_settings import conf
from common.auth import (
    get_current_user,
    get_session,
    set_current_user,
    requires_authentication,
    requires_unauthentication,
    remove_current_user, 
    exec_login
)

#    from common.auth import set_auth_cookie, delete_auth_cookie,
from common.common import (
    is_valid_name,
    is_valid_email,
    is_valid_password,
    coalesce,
    find_first,
    all_except,
)
from data.models import UserAccount
from services import (
    item_service as iserv,
    user_service as userv,
    settings_service as setserv,
)
from services.user_service import get_user_by_email, update_user_account


################################################################################
##      SETTINGS FOR THIS VIEW and Constants
################################################################################

ADDRESS_LINE_SIZE = 60
ZIP_CODE_SIZE = 20
LIST_CATEGORY_COUNT = 11
LOCATION_DISTRICT_COUNT = 21


################################################################################
##      Create an instance of the router
################################################################################

router = APIRouter(prefix='/account')


################################################################################
##      Define a route for the account page / update account
################################################################################

@router.get('/', dependencies = [Depends(requires_authentication)])
@template()
async def account():
    return account_viewmodel()
    
def account_viewmodel():
    user = get_current_user()
    assert user is not None
       
    return ViewModel(
        selected_menu = '',
        name = user.name,
        user = userv.get_user_actual_by_id(user.user_id),
        email_addr = user.email_addr,
        items_images_url = conf('ITEMS_IMAGES_URL'),     
        users_images_url = conf('USERS_IMAGES_URL'),
        list_user_items = userv.list_user_item(user.user_id),
        current = "account",      
    )
        

################################################################################
##     Handling the POST request and view model for account page / update account
################################################################################

@router.post('/', dependencies = [Depends(requires_authentication)])
@template(template_file='account/account.html')
async def update_account(request: Request):
    vm = await update_account_viewmodel(request)
    
    if vm.error:
        return vm
    
    return responses.RedirectResponse(url='/', status_code = status.HTTP_302_FOUND)


async def update_account_viewmodel(request: Request):
    
    
    def new_or_none(form_field: str) -> str | None:
        old = getattr(user, form_field)
        new = form_field_as_str(form_data, form_field).strip()
        if new is None or new == old:
            return None
        return new
    
    user = get_current_user()
    assert user is not None
    form_data = await request.form()
    
    vm = ViewModel(
        error_msg = '',
        name = user.name,
        email_addr = form_field_as_str(form_data, 'email_addr').strip(),
        address_line = form_field_as_str(form_data, 'address_line').strip(),
        address_line_maxlength = ADDRESS_LINE_SIZE,
        zip_code = form_field_as_str(form_data, 'zip_code').strip(),
        zip_code_maxlength = ZIP_CODE_SIZE,
        choose_file_msg = "Selecionar ficheiro",
    )
    
    current_password = form_field_as_str(form_data, 'current_password').strip(),
    new_password = form_field_as_str(form_data, 'new_password').strip(),
    new_email = new_or_none('email_addr')
    new_address_line = new_or_none('address_line')
    new_zip_code = new_or_none('zip_code')
    
    
    if not userv.password_matches(user, current_password):
        vm.error_msg = 'Palavra-passe errada!'
    elif new_email and not is_valid_email(new_email):
        vm.error_msg = f'Endereço de email {new_email} inválido!'
    elif new_email and userv.get_user_by_email(new_email):
        vm.error_msg = f'O endereço de email {new_email} já está registado!'
    elif new_password and not is_valid_password(new_password):
        vm.error_msg = 'Nova palavra-passe inválida!'
    elif new_password and new_password == current_password:
        vm.error_msg = 'A nova palavra-passe não pode ser igual à anterior!'
    
    vm.error = bool(vm.error_msg)
    
    if not vm.error:
        userv.update_account(
            user.user_id,
            current_password,
            new_email,
            new_password,
            new_address_line,
            new_zip_code,
        )
    
        if file := form_field_as_file(form_data, 'profile_image'):
            async with upload_file_closing(file) as file_cm:
                if not file_cm.content_type:
                    raise ValueError(f"No content type for uploaded file {file.filename}")
                await userv.add_profile_image(
                   user.user_id,
                   file_cm,
                   content_type = file_cm.content_type,
                )
                
    return vm



def districts_viewmodel_info(selected_name_district: str) -> dict:
    all_districts = setserv.get_accepted_districts()
    key = lambda d: d.name
    selected_district = find_first(all_districts, selected_name_district, key = key)
    if selected_name_district != '' and not selected_district:
        raise ValueError(f"Selected district {selected_name_district} not found")
    other_districts = all_except(all_districts, selected_name_district, key = key)

    return dict(
        selected_district_name = selected_district.name if selected_district else '',
        other_districts = other_districts,
    )



################################################################################
##      Define a route and View model for the register page
################################################################################

@router.get('/register', dependencies = [Depends(requires_unauthentication)])
@template()
async def register():
    return register_viewmodel()


def register_viewmodel():
    name = get_session().get('name')
    email_addr = get_session().get('email_addr')
    return ViewModel(   
        selected_menu = '',
        current = "new",     
        name = name,
        name_status = 'disabled' if name else '',
        email_addr = email_addr,
        email_addr_status = 'disabled' if email_addr else '',
        password = '',
        checked = False,
        
    )


################################################################################
##     Handling the POST request and view model for registration
################################################################################

@router.post('/register', dependencies = [Depends(requires_unauthentication)])
@template(template_file='account/register.html')
async def post_register(request: Request):
    vm = await post_register_viewmodel(request)

    if vm.error:
        return vm
    
    return exec_login(vm.new_user_id)

    
    
async def post_register_viewmodel(request: Request) -> ViewModel:
    name = get_session().get('name')
    email_addr = get_session().get('email_addr')
    form_data = await request.form()
    vm = ViewModel(
        selected_menu = '',
        name = name if name else form_field_as_str(form_data, 'name'),
        name_status = 'disabled' if name else '',
        email_addr = email_addr if email_addr else form_field_as_str(form_data, 'email_addr'),
        email_addr_status = 'disabled' if email_addr else '',
        password = form_field_as_str(form_data, 'password'),
        new_user_id = None,
        checked = False,          
    )

    if not is_valid_name(vm.name):
        vm.error, vm.error_msg = True, 'Nome inválido!'
    elif not is_valid_email(vm.email_addr):
        vm.error, vm.error_msg = True, 'Endereço de email inválido!'
    elif not is_valid_password(vm.password):
        vm.error, vm.error_msg = True, 'Palavra-passe inválida!'
    elif userv.get_user_by_email(vm.email_addr):
        vm.error, vm.error_msg = True, f'O endereço de email {vm.email_addr} já está registado!'
    else:
        vm.error, vm.error_msg = False, ''

    if not vm.error:
        vm.new_user_id = userv.create_user_account(
            vm.name,
            vm.email_addr,
            vm.password,
        ).user_id

    return vm


################################################################################
##      Define a route and View model for the login page
################################################################################

@router.get('/login', dependencies = [Depends(requires_unauthentication)])
@template()
async def login():
    return login_viewmodel()
    
def login_viewmodel():
    return ViewModel(
        selected_menu = '',
        email_addr = '',
        password = '',
        external_auth_providers = setserv.get_external_auth_providers(),
    )
    

################################################################################
##     Handling the POST request and view model for login
################################################################################

@router.post('/login', dependencies = [Depends(requires_unauthentication)])
@template(template_file='account/login.html')
async def post_login(request: Request):
    vm = await post_login_viewmodel(request)

    if vm.error:
        return vm
    
    return exec_login(vm.user_id)


async def post_login_viewmodel(request: Request) -> ViewModel:
    form_data = await request.form()
    vm = ViewModel(
        selected_menu = '',
        email_addr = form_field_as_str(form_data, 'email_addr'),
        password = form_field_as_str(form_data, 'password'),
        user_id = None,
        external_auth_providers = setserv.get_external_auth_providers(),
    )

    if not is_valid_email(vm.email_addr):
        vm.error_msg = 'Palavra-passe errada ou utilizador inválido!'
    elif not is_valid_password(vm.password):
        vm.error_msg = 'Palavra-passe errada!'
    elif not (user := userv.authenticate_user_by_email(vm.email_addr, vm.password)):
        vm.error_msg = 'Palavra-passe errada ou utilizador inválido!'
    else:
        vm.error_msg = ''
        vm.user_id = user.user_id

    vm.error = bool(vm.error_msg)
    
    return vm

def exec_login(user_id: int) -> Response:
    set_current_user(user_id)
    response = responses.RedirectResponse(url = '/', status_code = status.HTTP_302_FOUND)
    return response



  
################################################################################
##      Define a route and View model for the logout page
################################################################################

@router.get('/logout', dependencies = [Depends(requires_authentication)])
async def logout():
    response = responses.RedirectResponse(url='/', status_code = status.HTTP_302_FOUND)
    remove_current_user()
    return response



################################################################################
##      Define a route and View model for the dashboard page and all pages submenus
################################################################################
    
@router.get('/profileSettings', dependencies = [Depends(requires_authentication)])
@template()
async def profileSettings():
    return profileSettings_viewmodel()
    
def profileSettings_viewmodel(error_msg = ''):
    user = get_current_user()
    assert user is not None
       
    vm = ViewModel(
        selected_menu = '',
        current = "edit",
        name = user.name,
        user = userv.get_user_actual_by_id(user.user_id),
        email_addr = user.email_addr,
        items_images_url = conf('ITEMS_IMAGES_URL'),     
        users_images_url = conf('USERS_IMAGES_URL'),
        districts_images_url = conf('DISTRICTS_IMAGES_URL'),
        location_district = setserv.get_accepted_district(),
        list_user_items = userv.list_user_item(user.user_id),
        address_line = coalesce(user.address_line, ''),
        address_line_maxlength = ADDRESS_LINE_SIZE,
        zip_code = coalesce(user.zip_code, ''),
        zip_code_maxlength = ZIP_CODE_SIZE,
        address_district = user.district_id,       
    )
    
    if error_msg != '':
        vm.error, vm.error_msg = True, error_msg
    return vm


@router.post('/update_profileSettings', dependencies = [Depends(requires_authentication)])
@template(template_file='account/profileSettings.html')
async def update_profileSettings(request: Request):
    form_data = await request.form()
    new_name = form_field_as_str(form_data, 'name')
    # todo: phone_number = form_field_as_str(form_data, 'phone_number')
    new_email_addr = form_field_as_str(form_data, 'email_addr')
    new_address_line = form_field_as_str(form_data, 'address_line')
    new_zip_code = form_field_as_str(form_data, 'zip_code')
    new_location = form_field_as_str(form_data, 'location')
    user = get_current_user()
    if not is_valid_name(new_name):
        error_msg = 'Nome inválido!'
    elif not is_valid_email(new_email_addr):
        error_msg = 'Endereço de email inválido!'
    elif get_user_by_email(new_email_addr) and get_user_by_email(new_email_addr)!=user:
        error_msg = 'Endereço de email já registado!'
    else:
        error_msg = ''
        userv.update_user_account(user_or_id=user.user_id, 
                                  new_name=new_name, 
                                  new_email=new_email_addr, 
                                  new_address_line=new_address_line, 
                                  new_zip_code = new_zip_code, 
                                  new_district_id=new_location
        )
        
        
    return profileSettings_viewmodel(error_msg)







@router.post('/update_password', dependencies = [Depends(requires_authentication)])
@template(template_file='account/profileSettings.html')
async def update_password(request: Request):
    form_data = await request.form()
    current_password = form_field_as_str(form_data, 'current_password')
    new_password = form_field_as_str(form_data, 'new_password')
    retype_new_password = form_field_as_str(form_data, 'retype_new_password')
    user = get_current_user()
    if not userv.password_matches(user, current_password):
        error_msg = 'Palavra-passe atual incorreta!'
    elif new_password != retype_new_password:
        error_msg = 'Palavra-passe nova e a sua verificação não são iguais!'
    elif not is_valid_password(new_password):
        error_msg = 'Palavra-passe nova inválida!'
    else:
        error_msg = ''
        userv.update_user_account(user_or_id=user.user_id, new_password=new_password, current_password=current_password)
        
        
    return profileSettings_viewmodel(error_msg)










ALLOWED_EXTENSIONS = {'jpeg', 'jpg', 'png'}
    
@router.post('/update_picture', dependencies = [Depends(requires_authentication)])
@template(template_file='account/profileSettings.html')
async def update_picture(file: UploadFile = File(...)):
    error_msg = ''
    pic = file
    user = get_current_user()
    

    filename = secure_filename(pic.filename)

    #save_path = os.path.join(conf('USERS_IMAGES_URL'), filename)
    file_ext = os.path.splitext(filename)[1].lstrip('.').lower()

    if not filename:
        return profileSettings_viewmodel(error_msg = "Nenhuma imagem foi carregada!")

    if file_ext not in ALLOWED_EXTENSIONS:
        return profileSettings_viewmodel(error_msg = "Apenas são permitidos ficheiros do tipo JPEG, JPG e PNG.")

    with open(f"./static/assets/images/users/{filename}", "wb") as f:
        f.write(pic.file.read())
    # Process the uploaded file as needed (e.g., update user profile)
    userv.add_profile_image_to_user(user.user_id,filename)
    return profileSettings_viewmodel()



















@router.get('/myAds', dependencies = [Depends(requires_authentication)])
@template()
async def myAds():
    return myAds_viewmodel()
    
def myAds_viewmodel():
        return ViewModel(
        error = None,
        current = "ads",
    )
    
    
    
@router.get('/favoritesAds', dependencies = [Depends(requires_authentication)])
@template()
async def favoritesAds():
    return favoritesAds_viewmodel()
    
def favoritesAds_viewmodel():
        return ViewModel(
        error = None,
        current = "fav",
    )
    
    
    
@router.get('/newAdPost', dependencies = [Depends(requires_authentication)])
@template()
async def newAdPost():
    return newAdPost_viewmodel()
   
def newAdPost_viewmodel():
    return ViewModel(
        list_category = setserv.get_accepted_category(),
        location_district = setserv.get_accepted_district(),
        current = "new",
    )
    
    
    
@router.get('/messages', dependencies = [Depends(requires_authentication)])
@template()
async def messages():
    return messages_viewmodel()
    
def messages_viewmodel():
        return ViewModel(
        error = None,
        current = "msgs",
    )
    
    
    
@router.get('/deleteAccount', dependencies = [Depends(requires_authentication)])
@template()
async def deleteAccount():
    return deleteAccount_viewmodel()
    
def deleteAccount_viewmodel():
        return ViewModel(
        error = None,
        current = "close",
    )

        
        
@router.get('/mailSuccess', dependencies = [Depends(requires_authentication)])
@template()
async def mailSuccess():
    return mailSuccess_viewmodel()
    
def mailSuccess_viewmodel():
        return ViewModel(
        error = None,
    )