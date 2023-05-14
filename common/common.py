__all__ = (
    'MIN_DATE',
    'is_valid_name',
    'is_valid_email',
    'is_valid_password',
    'is_valid_iso_date',
    'is_valid_birth_date',
    'find_in'
)


from datetime import date
import re
from typing import Any, Iterable



MIN_DATE = date.fromisoformat('1920-01-01')





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
    else:  # no exception:
        return True


def is_valid_birth_date(birth_date: str) -> bool:
    return (is_valid_iso_date(birth_date) 
        and date.fromisoformat(birth_date) >= MIN_DATE)


def find_in(iterable: Iterable, predicate) -> Any | None:
    return next((obj for obj in iterable if predicate(obj)), None)

