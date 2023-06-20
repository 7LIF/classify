################################################################################
##      Importing necessary modules
################################################################################

from datetime import date
from typing import List
import uuid
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
from data.models import Item, PHONE_NUMBER_SIZE, UserAccount
from services import (
    item_service as iserv,
    user_service as userv,
    settings_service as setserv,
)
from services.user_service import get_msg, get_user_by_email, send_msg, update_user_account, user_has_favorite


################################################################################
##      SETTINGS FOR THIS VIEW and Constants
################################################################################

ADDRESS_LINE_SIZE = 60
ZIP_CODE_SIZE = 20
LIST_CATEGORY_COUNT = 11
LOCATION_DISTRICT_COUNT = 21
ALLOWED_EXTENSIONS = {'jpeg', 'jpg', 'png'}


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
        current = "account",
        items_images_url = conf('ITEMS_IMAGES_URL'),     
        users_images_url = conf('USERS_IMAGES_URL'),
        user = userv.get_user_actual_by_id(user.user_id),
        name = user.name,
        email_addr = user.email_addr,
        list_user_items = userv.list_user_item(user.user_id),        
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
##      Define a route and View model for the profileSettings page
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
        phone_number = user.phone_number,
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
    new_phone_number = form_field_as_str(form_data, 'phone_number')
    new_email_addr = form_field_as_str(form_data, 'email_addr')
    new_address_line = form_field_as_str(form_data, 'address_line')
    new_zip_code = form_field_as_str(form_data, 'zip_code')
    new_location = form_field_as_str(form_data, 'location')
    user = get_current_user()
    if not is_valid_name(new_name):
        error_msg = 'Nome inválido!'
    elif len(new_phone_number)!=PHONE_NUMBER_SIZE:
        error_msg = 'Insira um número de de telefone válido!'
    elif not is_valid_email(new_email_addr):
        error_msg = 'Endereço de email inválido!'
    elif get_user_by_email(new_email_addr) and get_user_by_email(new_email_addr).user_id!=user.user_id:
        error_msg = 'Endereço de email já registado!'
    else:
        error_msg = ''
        userv.update_user_account(user_or_id=user.user_id, 
                                  new_name=new_name, 
                                  new_phone_number = new_phone_number,
                                  new_email=new_email_addr, 
                                  new_address_line=new_address_line, 
                                  new_zip_code = new_zip_code, 
                                  new_district_id=new_location
        )
        
    return profileSettings_viewmodel(error_msg)


    
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




################################################################################
##      Define a route and View model for the myAds page
################################################################################

@router.get('/myAds', dependencies = [Depends(requires_authentication)])
@template()
async def myAds():
    return myAds_viewmodel()
    
def myAds_viewmodel(error_msg = ''):
    user = get_current_user()
    assert user is not None
    vm = ViewModel(
        selected_menu = '',
        current = "ads",
        users_images_url = conf('USERS_IMAGES_URL'),
        items_images_url = conf('ITEMS_IMAGES_URL'),
        user = userv.get_user_actual_by_id(user.user_id),
        list_user_items = userv.list_user_item(user.user_id),
        name = user.name,
    )
    if error_msg != '':
        vm.error, vm.error_msg = True, error_msg
    return vm


@router.get('/delete_Ad', dependencies=[Depends(requires_authentication)])
@template(template_file='account/myAds.html')
async def delete_Ad(request: Request):
    user = get_current_user()
    assert user is not None
    
    item_id = request.query_params.get('item_id')
    if not iserv.item_belongs_to_user(item_id, user.user_id):
        return myAds_viewmodel(error_msg = 'Sem permissões para apagar esse item')
    elif item_id:
        iserv.delete_item(item_id)
    return myAds_viewmodel()
    



################################################################################
##      Define a route and View model for the newAdPost page
################################################################################    
    
@router.get('/newAdPost', dependencies = [Depends(requires_authentication)])
@template()
async def newAdPost(request: Request):     
    return newAdPost_viewmodel(request)


def newAdPost_viewmodel(request: Request,error_msg = '', success = False):
    user = get_current_user()
    assert user is not None   
    item_id = request.query_params.get('item_id')
     
    if item_id and  iserv.item_belongs_to_user(item_id,user.user_id):           
        item = iserv.get_item_by_id(item_id)
        address_line = item.address_line
        zip_code = item.zip_code
        district = item.district_id
        title=item.title
        add_subcategory = item.subcategory_id
        price = item.price
        files1 = item.main_image_url        
        files2 = item.image1_url        
        files3 = item.image2_url        
        files4 = item.image3_url        
        files5 = item.image4_url   
        description = item.description
        edit = True  
        success_msg = "Anuncio alterado com sucesso"
    else:
        if item_id:
            error_msg = "Não tem permissões para editar este Item"
        address_line = user.address_line
        zip_code = user.zip_code
        district = user.district_id
        title=''
        add_subcategory = ''
        price = ''
        files1 = ''      
        files2 = ''      
        files3 = ''      
        files4 = ''      
        files5 = '' 
        description = ''
        edit=False
        item_id=""
        success_msg = "Anuncio adicionado com sucesso"
    vm = ViewModel(
        selected_menu = '',
        current = "new",
        users_images_url = conf('USERS_IMAGES_URL'),
        items_images_url = conf('ITEMS_IMAGES_URL'),
        list_subcategory = setserv.get_accepted_subcategory(),
        user = userv.get_user_actual_by_id(user.user_id),
        list_user_items = userv.list_user_item(user.user_id),
        item_id=item_id,
        name = user.name,
        address_line = address_line,
        zip_code = zip_code,
        title=title,
        price = price,
        add_subcategory = add_subcategory,
        address_district = district,
        files1 = files1,
        files2 = files2 ,     
        files3 = files3 ,     
        files4 = files4 ,     
        files5 = files5,
        description = description,
        location_district = setserv.get_accepted_district(),
        checked = False,
        success = False,
        edit = edit,
        success_msg=success_msg
    )
    if error_msg != '':
        vm.error, vm.error_msg = True, error_msg
    if success:
        vm.success=True,
    return vm
    
def upload_item_image(pic) ->str | None:    
    filename = secure_filename(pic.filename)
    file_ext = os.path.splitext(filename)[1].lstrip('.').lower()
    # Generate a unique filename for each file
    unique_filename = f"{uuid.uuid4().hex}{os.path.splitext(filename)[1]}"
    save_path = os.path.join("./"+conf('ITEMS_IMAGES_URL'), unique_filename)
    if not filename:
        return ''
    if file_ext not in ALLOWED_EXTENSIONS:
        return None

    with open(save_path, "wb") as f:
        f.write(pic.file.read())
    return unique_filename

@router.post('/create_Ad', dependencies=[Depends(requires_authentication)])
@template(template_file='account/newAdPost.html')
async def create_Ad(request: Request, files1: UploadFile = File(...), files2: UploadFile = File(...), files3: UploadFile = File(...), files4: UploadFile = File(...),files5: UploadFile = File(...),):
    user = get_current_user()
    assert user is not None
    form_data = await request.form()  
    title = form_field_as_str(form_data, 'title')  
    price = form_field_as_str(form_data, 'price')
    main_image_url =''
    image1_url = ''
    image2_url = ''
    image3_url = ''
    image4_url = ''
    address_line = form_field_as_str(form_data, 'address_line')
    zip_code = form_field_as_str(form_data, 'zip_code')
    district_id = form_field_as_str(form_data, 'location')
    subcategory_id = form_field_as_str(form_data, 'subcategory')
    price = form_field_as_str(form_data, 'price')
    description= form_field_as_str(form_data, 'message')
    user_id = user.user_id   
    
    if not title:
       error_msg = 'Insira um título'
    elif not subcategory_id:
       error_msg = 'Selecione uma subcategoria' 
    elif not price:
       error_msg = 'Insira o preço'  
    elif not description:
       error_msg = 'Insira a descrição'
    elif not district_id:
       error_msg = 'Selecione um distrito'
    elif not files1.filename: 
       error_msg = 'Adicione a foto principal'  
    else:
       error_msg = ''

    
    

    file_list = [files1, files2, files3, files4, files5]
    image_urls = []

    for files in file_list:
        image_url = upload_item_image(files)
        if image_url is None:
            error_msg = "Apenas são permitidos ficheiros do tipo JPEG, JPG e PNG"
            break
        image_urls.append(image_url)
    
    if error_msg == '':
        main_image_url = image_urls[0]
        image1_url = image_urls[1]
        image2_url = image_urls[2]
        image3_url = image_urls[3]
        image4_url = image_urls[4]
    
    if error_msg == '':
        new_ad = iserv.create_item(
            title,
            description,  
            main_image_url,
            image1_url,
            image2_url,
            image3_url,
            image4_url,
            address_line,
            zip_code,
            district_id,
            subcategory_id,
            price,
            user_id,
        )
        return newAdPost_viewmodel(request,error_msg = error_msg, success= True)
    
    return newAdPost_viewmodel(request,error_msg = error_msg)
    


@router.post('/edit_Ad', dependencies=[Depends(requires_authentication)])
@template(template_file='account/newAdPost.html')
async def create_Ad(request: Request, files1: UploadFile = File(...), files2: UploadFile = File(...), files3: UploadFile = File(...), files4: UploadFile = File(...),files5: UploadFile = File(...)):
    
    item_id = request.query_params.get('item_id')
    user = get_current_user()
    assert user is not None
    form_data = await request.form()  
    title = form_field_as_str(form_data, 'title')  
    price = form_field_as_str(form_data, 'price')
    address_line = form_field_as_str(form_data, 'address_line')
    zip_code = form_field_as_str(form_data, 'zip_code')
    district_id = form_field_as_str(form_data, 'location')
    subcategory_id = form_field_as_str(form_data, 'subcategory')
    price = form_field_as_str(form_data, 'price')
    description= form_field_as_str(form_data, 'message')
    user_id = user.user_id   
    main_image_url =''
    image1_url = ''
    image2_url = ''
    image3_url = ''
    image4_url = ''
    
    if not title:
       error_msg = 'Insira um título'
    elif not subcategory_id:
       error_msg = 'Selecione uma subcategoria' 
    elif not price:
       error_msg = 'Insira o preço'  
    elif not description:
       error_msg = 'Insira a descrição'
    elif not district_id:
       error_msg = 'Selecione um distrito' 
    else:
       error_msg = ''    
    
    file_list = [files1, files2, files3, files4, files5]
    image_urls = []

    for files in file_list:
        image_url = upload_item_image(files)
        if image_url is None:
            error_msg = "Apenas são permitidos ficheiros do tipo JPEG, JPG e PNG"
            break
        image_urls.append(image_url)
    
    if error_msg == '':
        main_image_url = image_urls[0]
        image1_url = image_urls[1]
        image2_url = image_urls[2]
        image3_url = image_urls[3]
        image4_url = image_urls[4]
   
    
    if error_msg == '':
        new_ad = iserv.edit_item(
            item_id=item_id,
            title= title,
            description= description,
            main_image_url =main_image_url,
            image1_url = image1_url,
            image2_url = image2_url,
            image3_url = image3_url,
            image4_url = image4_url, 
            address_line= address_line,
            zip_code=zip_code,
            district_id=district_id,
            subcategory_id=subcategory_id,
            price=price,
        )
        return newAdPost_viewmodel(request,error_msg = error_msg, success= True)
    
    return newAdPost_viewmodel(request,error_msg = error_msg) 


@router.post("/removeImage")
async def removeImage(request_data: dict):
    # Process the AJAX request data
    # You can access the request data using the `request_data` parameter
    # Perform necessary operations and return the response
    user = get_current_user()
    assert user is not None
    type_image = request_data['type']
    item_id = request_data['item']
    img = request_data['dataImg']
    if type_image == "main_image_url":
        return "success"
    if not iserv.item_belongs_to_user(item_id,user.user_id):
        return "Nao tem permissoes para editar esse item"
    if iserv.remove_image_from_item(item_id,user.user_id,img,type_image):

        response_data = "success"
    else:
        response_data = "something went wrong"
    return response_data


@router.post("/toggle_favorite")
async def toggle_favorite(request_data: dict):
    # Process the AJAX request data
    # You can access the request data using the `request_data` parameter
    # Perform necessary operations and return the response
    user = get_current_user()
    assert user is not None
    item_id = request_data['item_id']
    if not userv.user_has_favorite(user.user_id,item_id):
        userv.add_favorite_item_to_user(user.user_id,item_id)
        return "add"
    else:
        userv.remove_favorite_item_from_user(user_id=user.user_id,item_id=item_id)
        return "remove"
    
    
@router.get("/remove_favorite")
@template(template_file='account/favoritesAds.html')
async def remove_favorite(request: Request):
    user = get_current_user()
    assert user is not None
    
    item_id = request.query_params.get('item_id')
    userv.remove_favorite_item_from_user(user_id=user.user_id,item_id=item_id)
    return favoritesAds_viewmodel() 
    
       
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    




















################################################################################
##      Define a route and View model for the deleteAccount page
################################################################################  
    
@router.get('/deleteAccount', dependencies = [Depends(requires_authentication)])
@template()
async def deleteAccount():
    return deleteAccount_viewmodel()
    
def deleteAccount_viewmodel():
        return ViewModel(
        error = None,
        current = "close",
    )



################################################################################
##      Define a route and View model for the mailSuccess page
################################################################################        
        
@router.get('/mailSuccess', dependencies = [Depends(requires_authentication)])
@template()
async def mailSuccess():
    return mailSuccess_viewmodel()
    
def mailSuccess_viewmodel():
        return ViewModel(
        error = None,
    )
        
        
################################################################################
##      Define a route and View model for the favoritesAds page
################################################################################


@router.get('/favoritesAds', dependencies = [Depends(requires_authentication)])
@template()
async def favoritesAds():
    return favoritesAds_viewmodel()
    
def favoritesAds_viewmodel(error_msg = ''):
    user = get_current_user()
    assert user is not None
    vm = ViewModel(
        selected_menu = '',
        current = "fav",
        users_images_url = conf('USERS_IMAGES_URL'),
        items_images_url = conf('ITEMS_IMAGES_URL'),
        user = userv.get_user_actual_by_id(user.user_id),
        list_user_items = userv.list_user_item(user.user_id),
        name = user.name,
        items = userv.get_user_favorites(user.user_id)
    )
    if error_msg != '':
        vm.error, vm.error_msg = True, error_msg
    return vm


################################################################################
##      Define a route and View model for the messages page
################################################################################

@router.get('/messages', dependencies = [Depends(requires_authentication)])
@template()
async def messages():
    return messages_viewmodel()
    
def messages_viewmodel(error_msg = ''):
    user = get_current_user()
    assert user is not None

    chatrooms_messages = userv.get_chatrooms(user.user_id)
    chatrooms={}
    count =0
    for message in chatrooms_messages :
        if message.recipient_id == user.user_id:
            other_user = userv.get_user_by_id(message.sender_id)
        else:
            other_user =  userv.get_user_by_id(message.recipient_id)
        chatrooms[count] = {}
        chatrooms[count]["message"] = message
        chatrooms[count]["item"] = iserv.get_item_by_id(message.item_id)
        chatrooms[count]["other_user"] = other_user
        chatrooms[count]["unread"] = userv.unread_count(user.user_id,other_user.user_id,message.item_id)
        count+=1

    vm = ViewModel(
        selected_menu = '',
        current = "msgs",
        users_images_url = conf('USERS_IMAGES_URL'),
        items_images_url = conf('ITEMS_IMAGES_URL'),
        user = userv.get_user_actual_by_id(user.user_id),
        name = user.name,
        chatrooms = chatrooms
    )
    if error_msg != '':
        vm.error, vm.error_msg = True, error_msg
    return vm


@router.get('/chat', dependencies = [Depends(requires_authentication)])
@template(template_file='account/chat.html')
async def chat(request: Request):
    user_2 = userv.get_user_actual_by_id(request.query_params.get('user'))
    item = request.query_params.get('item')
    return chat_viewmodel(user_2,item)
    
def chat_viewmodel( user_2,item):
    user = get_current_user()
    assert user is not None
    
    userv.read_messages(user.user_id,user_2.user_id,item)
    return ViewModel(
        selected_menu = '',
        current = "msgs",
        user = userv.get_user_actual_by_id(user.user_id),
        users_images_url = conf('USERS_IMAGES_URL'),
        user_2= user_2,
        item=iserv.get_item_by_id(item),
        chat_messages = userv.get_all_chat_msg(user1_id=user.user_id,user2_id= user_2.user_id, item_id=item),
        name=user.name, 
    )


@router.post("/chatroom")
async def chatroom(request_data: dict):
    # Process the AJAX request data
    # You can access the request data using the `request_data` parameter
    # Perform necessary operations and return the response
    user = get_current_user()
    assert user is not None
    item_id = request_data['item']
    user2 = request_data['user2']
    message = request_data['message']
    userv.send_msg(user.user_id,user2,item_id,message)
    new_message = userv.get_msg(user.user_id,user2,item_id,message)
    return_args = {}
    if new_message:
        return_args["status"] = "success"
        return_args["image"] = conf('USERS_IMAGES_URL')+"/"+userv.get_user_actual_by_id(user.user_id).profile_image
        return_args["message"] = message
        return_args["time"] = new_message.date_sent
        return_args["id"] = new_message.id
    else:
        return_args["status"] = "fail"

    return return_args


@router.post("/update_messages_live")
async def update_messages_live(request_data: dict):
    user = get_current_user()
    assert user is not None
    item_id = request_data['item']
    user2 = request_data['user2']
    msg_id = request_data['last_id']
    new_messages = userv.get_new_msgs(user.user_id,user2,item_id,msg_id)
    return_args = {}
    count = 0
    if new_messages:
        for new_message in new_messages:
            return_args[count] = {}
            return_args[count]["status"] = "success"
            return_args[count]["image"] = conf('USERS_IMAGES_URL')+"/"+userv.get_user_actual_by_id(new_message.sender_id).profile_image
            return_args[count]["message"] = new_message.message
            return_args[count]["time"] = new_message.date_sent
            return_args[count]["id"] = new_message.id
            count+=1
    else:        
        return_args[0] = {}
        return_args[0]["status"] = "fail"

    return return_args

