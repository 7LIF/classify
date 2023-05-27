################################################################################
##      Specifies the public interface of this module
################################################################################

__all__ = (
    'exec_login',
    'requires_authentication',
    'requires_unauthentication',
    'get_session',
    'get_current_user',
    'set_current_user',
    'remove_current_user',  
)


    #'set_auth_cookie',
    #'get_auth_from_cookie',
    #'delete_auth_cookie',
    #'hash_cookie_value',  

################################################################################
##      Importing necessary modules
################################################################################

from hashlib import sha512
from typing import Any
from fastapi import FastAPI, HTTPException, status, responses
from fastapi.requests import Request
from fastapi.responses import Response
from starlette.middleware.sessions import SessionMiddleware
from config_settings import config_value
from data.models import User
from services import (
    item_service as iserv,
    user_service as userv,
    settings_service as setserv,
)
from common.fastapi_utils import global_request



################################################################################
##      Constants
################################################################################

#AUTH_COOKIE_NAME = 'user_id'
#SESSION_COOKIE_MAX_AGE = 86400_00          # 86400 seconds =~ 1 day // 86400_00 seconds =~ 100 days
#SECRET_KEY = '8e10d234a1f8eb6f9dd6dfc3a325a0613ad2e620e5b8844cb011470492422bee'


SESSION_COOKIE_NAME = config_value('SESSION_COOKIE_NAME')
SESSION_SECRET_KEY = config_value('SESSION_SECRET_KEY')
SESSION_COOKIE_HTTPONLY = config_value('SESSION_COOKIE_HTTPONLY')
SESSION_COOKIE_SECURE = config_value('SESSION_COOKIE_SECURE')
SESSION_COOKIE_SAMESITE = config_value('SESSION_COOKIE_SAMESITE')
SESSION_COOKIE_MAX_AGE = config_value('SESSION_COOKIE_MAX_AGE')
SESSION_ID_LEN = 64   # in chars





def exec_login(user_id: int) -> Response:
    set_current_user(user_id)
    response = responses.RedirectResponse(url = '/', status_code = status.HTTP_302_FOUND)
    return response


def requires_authentication():
    if not get_current_user():
        raise HTTPUnauthorizedAccess(detail = 'This area requires authentication.')
    
    
class HTTPUnauthorizedAccess(HTTPException):
    def __init__(self, *args, **kargs):
        super().__init__(status_code = status.HTTP_401_UNAUTHORIZED, *args, **kargs)   
    
    


def requires_unauthentication():
    if get_current_user():
        raise HTTPUnauthenticatedOnly(detail = 'This is a public area only.')


class HTTPUnauthenticatedOnly(HTTPUnauthorizedAccess):
    pass




def add_session_middleware(app: FastAPI):
    app.add_middleware(
        SessionMiddleware,
        session_cookie = SESSION_COOKIE_NAME,
        secret_key = SESSION_SECRET_KEY,
        same_site = SESSION_COOKIE_SAMESITE,
        https_only = SESSION_COOKIE_SECURE,
        max_age = SESSION_COOKIE_MAX_AGE,
    )





def get_session(session_attr = 'session') -> Any:
    request = global_request.get()
    return getattr(request, session_attr)






def get_current_user(request: Request | None = None) -> User | None:
    if request is None:
        request  = global_request.get()
    user_id = request.session.get('user_id')
    if isinstance(user_id, int):
        return userv.get_user_by_id(user_id)
    return None




def set_current_user(user_id: int):
    request = global_request.get()
    request.session['user_id'] = user_id




def remove_current_user():
    request = global_request.get()
    del request.session['user_id']



































    """
def set_auth_cookie(response: Response, user_id: int):
    cookie_value = f'{str(user_id)}:{hash_cookie_value(str(user_id))}'
    response.set_cookie(
        AUTH_COOKIE_NAME,
        cookie_value,
        secure = False,             # True -> a cookie só é enviada por HTTPs
        httponly = True,
        samesite = 'lax',
        max_age= SESSION_COOKIE_MAX_AGE,
    )






def get_auth_from_cookie(request: Request) -> int | None:
    if not (cookie_value := request.cookies.get(AUTH_COOKIE_NAME)):
        return None
    
    parts = cookie_value.split(':')
    if len(parts) != 2:
        return None
    
    user_id, hash_value = parts
    hash_check_value = hash_cookie_value(user_id)
    if hash_value != hash_check_value:
        print("Warning: hash mismatch. Invalid cookie value!")
        return None
    
    return int(user_id) if user_id.isdigit() else None







def delete_auth_cookie(response: Response):
    response.delete_cookie(AUTH_COOKIE_NAME)
    



def hash_cookie_value(cookie_value: str) -> str:
    return sha512(f'{cookie_value}{SECRET_KEY}'.encode('utf-8')).hexdigest()

    """


