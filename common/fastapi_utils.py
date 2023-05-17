################################################################################
##      Specifies the public interface of this module
################################################################################

__all__ = (
    'global_request',
    'add_global_request_middleware',
    'form_field_as_str',
    'form_field_as_file',
    'upload_file_closing',
)



################################################################################
##      Importing necessary modules
################################################################################

from contextvars import ContextVar
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, Request, UploadFile
from fastapi.datastructures import FormData
from starlette.datastructures import UploadFile as StarletteUploadFile



################################################################################
##      ContextVar instance to hold the current request object globally
################################################################################

global_request : ContextVar[Request] = ContextVar("global_request")



################################################################################
##      Middleware function that adds the request object to the global context
################################################################################

# https://fastapi.tiangolo.com/tutorial/middleware/#middleware

def add_global_request_middleware(app: FastAPI):
    @app.middleware("http")
    async def global_request_middleware(request: Request, call_next):
        global_request.set(request)
        response = await call_next(request)
        return response
    return global_request_middleware        # this returns the inner function



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

def form_field_as_file(form_data: FormData, field_name: str) -> StarletteUploadFile:
    field_value = form_data[field_name]
    if isinstance(field_value, StarletteUploadFile):
        return field_value
    raise TypeError(f'Form field {field_name} type is not {StarletteUploadFile.__name__}')



@asynccontextmanager
async def upload_file_closing(file_obj: UploadFile | StarletteUploadFile) -> AsyncGenerator[UploadFile | StarletteUploadFile, None]:
    try:
        yield file_obj
    finally:
        await file_obj.close()
        