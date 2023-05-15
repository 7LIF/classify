################################################################################
##      Specifies the public interface of this module
################################################################################

__all__ = (
    'form_field_as_str',
    'form_field_as_file',
)



################################################################################
##      Importing necessary modules
################################################################################

from contextvars import ContextVar
from fastapi import FastAPI, Request, UploadFile
from fastapi.datastructures import FormData



################################################################################
##      ContextVar instance to hold the current request object globally
################################################################################

global_request : ContextVar[Request] = ContextVar("global_request")



################################################################################
##      Middleware function that adds the request object to the global context
################################################################################

def add_global_request_middleware(app: FastAPI):
    # https://fastapi.tiangolo.com/tutorial/middleware/#middleware
    @app.middleware("http")
    async def global_request_middleware(request: Request, call_next):
        global_request.set(request)
        response = await call_next(request)
        return response

    return global_request_middleware  # this returns the inner function



################################################################################
##      Takes form data and field name as input and returns the field value 
##      as a string
################################################################################

def form_field_as_str(form_data: FormData, field_name: str) -> str:
    field_value = form_data[field_name]
    if isinstance(field_value, str):
        return field_value
    raise TypeError(f'Form field {field_name} type is not str')



################################################################################
##      Takes form data and field name as input and returns the field value 
##      as an UploadFile object
################################################################################

def form_field_as_file(form_data: FormData, field_name: str) -> UploadFile:
    field_value = form_data[field_name]
    if isinstance(field_value, UploadFile):
        return field_value
    raise TypeError(f'Form field {field_name} type is not UploadFile')