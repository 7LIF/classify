################################################################################
##      Specifies the public interface of this module
################################################################################

__all__ = (
    'MIN_DATE',
    'GOOGLE_CLIENT_ID',
    'GOOGLE_CLIENT_SECRET',
    'GOOGLE_AUTH_URI',
    'GOOGLE_TOKEN_URI',
    'GOOGLE_REDIRECT_URI',
    'GOOGLE_SCOPE_REPLY',
    'GOOGLE_DISCOVERY_DOC_URL',
    'GOOGLE_GRANT_TYPE',
    'GOOGLE_JWKS_URI',
    'GOOGLE_ISS_URIS',
    'coalesce',
    'is_valid_name',
    'is_valid_email',
    'is_valid_password',
    'is_valid_iso_date',
    'make_test_regex_fn',
    'camel_to_snake_case',
    'pascal_to_snake_case',
    'snake_to_camel_case',
    'snake_to_pascal_case',
    'find_first',
    'find_first_if',
    'all_except',
    'random_str',
    'is_valid_iso_date',
    'is_valid_birth_date',
)



################################################################################
##      Importing necessary modules
################################################################################

import calendar, datetime, locale
import math, random, re, string, secrets
from datetime import date
from typing import Any, Callable, Iterable, Iterator
from config_settings import conf, config_value
import common.viewmodel
 
 
 
MIN_DATE = date.fromisoformat('1920-01-01')
 
 
 
################################################################################
##
##  SETTINGS
##
################################################################################

GOOGLE_CLIENT_ID = conf('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = conf('GOOGLE_CLIENT_SECRET')
GOOGLE_AUTH_URI = conf('GOOGLE_AUTH_URI')
GOOGLE_TOKEN_URI = conf('GOOGLE_TOKEN_URI')
GOOGLE_REDIRECT_URI = conf('GOOGLE_REDIRECT_URI')
GOOGLE_SCOPE_REPLY = conf('GOOGLE_SCOPE_REPLY')
GOOGLE_DISCOVERY_DOC_URL = conf('GOOGLE_DISCOVERY_DOC_URL')
GOOGLE_GRANT_TYPE = conf('GOOGLE_GRANT_TYPE')
GOOGLE_JWKS_URI = conf('GOOGLE_JWKS_URI')
GOOGLE_ISS_URIS = conf('GOOGLE_ISS_URIS')

SESSION_COOKIE_NAME = config_value('SESSION_COOKIE_NAME')
SESSION_SECRET_KEY = config_value('SESSION_SECRET_KEY')
SESSION_COOKIE_HTTPONLY = config_value('SESSION_COOKIE_HTTPONLY')
SESSION_COOKIE_SECURE = config_value('SESSION_COOKIE_SECURE')
SESSION_COOKIE_SAMESITE = config_value('SESSION_COOKIE_SAMESITE')
SESSION_COOKIE_MAX_AGE = config_value('SESSION_COOKIE_MAX_AGE')


################################################################################
##      MISCELLANEOUS
################################################################################

def coalesce(*args) -> Any:
    for arg in args:
        if arg is not None:
            return arg
    raise ValueError(f"All given arguments to {coalesce.__name__} are None")



################################################################################
##      REGULAR EXPRESSIONS
################################################################################

def make_test_regex_fn(regex: str):
    compiled_regex = re.compile(regex)
    def test_regex_fn(value: str) -> bool:
        return bool(re.fullmatch(compiled_regex, value))
    return test_regex_fn



################################################################################
##      VALIDATIONS
################################################################################

def is_valid_name(name: str) -> bool:
    parts = name.split()
    return len(parts) >= 2 and all(part.isalpha() and len(part) >= 2 for part in parts)


is_valid_email = make_test_regex_fn(
    r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
)


is_valid_password = make_test_regex_fn(
    r'[0-9a-zA-Z$#?!.]{3,10}'      # for testing purposes
    # r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[#$%&?!(){}/:;<>.,-_]).{6,16}$'
)


def is_valid_iso_date(iso_date: str) -> bool:
    try:
        date.fromisoformat(iso_date)
    except ValueError:
        return False
    else:
        return True



def is_valid_birth_date(birth_date: str) -> bool:
    return (is_valid_iso_date(birth_date) 
        and date.fromisoformat(birth_date) >= MIN_DATE)




def format_date(data):
    locale.setlocale(locale.LC_ALL, 'pt')
    day = data.day
    month = data.strftime('%B')
    year = data.year
    return f'{day} de {month} de {year}'



################################################################################
##      ITERABLES AND SEQUENCES
################################################################################

KeyFunction = Callable[[Any], Any]
Predicate = Callable[[Any], bool]

def find_first(
        iterable: Iterable,
        item: Any, 
        *, 
        key: KeyFunction = lambda x: x,
) -> Any | None:
    return next((obj for obj in iterable if key(obj) == item), None)


def find_first_if(                                          # def find_in
        iterable: Iterable,
        predicate: Predicate, 
) -> Any | None:
    return next((obj for obj in iterable if predicate(obj)), None)


def all_except(
        iterable: Iterable,
        item: Any, 
        *, key: KeyFunction = lambda x: x,
) -> Iterator:
    return (obj for obj in iterable if key(obj) != item)



################################################################################
##      STRINGs
################################################################################

def camel_to_snake_case(ident: str) -> str:
    """
    abcXpto  -> abc_xpto
    abc      -> abc
    abcXYpto -> abc_x_ypto
    """
    return ''.join((f'_{ch.lower()}' if ch.isupper() else ch) for ch in ident)


def pascal_to_snake_case(ident: str) -> str:
    """
    AbcXpto  -> abc_xpto
    Abc      -> abc
    AbcXYpto -> abc_x_ypto
    """
    return camel_to_snake_case(ident).lstrip('_')


def snake_to_camel_case(ident: str) -> str:
    """
    abc_xpto    -> abcXpto
    abc         -> abc
    abc_x_ypto  -> abcXYpto
    abc____xpto -> abcXpto
    abc_        -> abc
    abc__       -> abc
    """
    new_ident = snake_to_pascal_case(ident)
    return new_ident[0].lower() + new_ident[1:]


def snake_to_pascal_case(ident: str) -> str:
    """
    abc_xpto    -> AbcXpto
    abc         -> Abc
    abc_x_ypto  -> AbcXYpto
    abc____xpto -> AbcXpto
    abc_        -> Abc
    abc__       -> Abc
    """
    tokens = ident.split('_')
    return ''.join(
        (token[0].upper() + token[1:] if token else '') for token in tokens
    )


def is_ascii(txt: str) -> bool:
    try:
        txt.encode('ascii')
    except UnicodeEncodeError:
        return False
    else:
        return True


################################################################################
##      RANDOM
################################################################################

def random_str(length: int) -> str:
    return ''.join(random.choices(string.ascii_letters + '0123456789', k = length))



# Recommended by Google OAuth documentation
def secure_random_str(length: int) -> str:
    return secrets.token_hex(math.ceil(length / 2))[:length]        # return hashlib.sha256(os.urandom(1024)).hexdigest()




