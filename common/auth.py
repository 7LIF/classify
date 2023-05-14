all = (
    'set_auth_cookie',
    'hash_password',
)


from hashlib import sha512
from fastapi import Response


AUTH_COOKIE_NAME = 'user_id'
SESSION_COOKIE_MAX_AGE = 86400_00          # 86400 seconds = 1 day // 86400_00 seconds = 100 days
SECRET_KEY = '8e10d234a1f8eb6f9dd6dfc3a325a0613ad2e620e5b8844cb011470492422bee'


def set_auth_cookie(response: Response, user_id: int):
    cookie_value = f'{str(user_id)}:{hash_cookie_value(str(user_id))}'
    response.set_cookie(
        AUTH_COOKIE_NAME,
        cookie_value,
        secure = False,
        httponly = True,
        samesite = 'lax',
        max_age= SESSION_COOKIE_MAX_AGE,
    )


def hash_cookie_value(cookie_value: str) -> str:
    return sha512(f'{cookie_value}{SECRET_KEY}'.encode('utf-8')).hexdigest()


# simula - TEMPORARIAMENTE
def hash_password(password: str) -> str:
    return password + '-hash-pwd'