from datetime import date
from random import randrange
from typing import List
from common.hash_password import hash_password
from common.common import is_valid_email, find_in
from data.models import User, Testimonial



# variável que simula a base de dados - TEMPORARIAMENTE
_users = []




def create_account(
    name: str,
    email_addr: str,
    password: str,
):
    user = User(
        randrange(10_000, 100_000),  # id
        name,
        email_addr,
        hash_password(password),
    )
    _users.append(user)
    return user





def get_user_by_id(user_id: int) -> User | None:
    return find_in(_users, lambda user: user.id == user_id)




def get_user_by_email(email_addr: str) -> User | None:
    if not is_valid_email(email_addr):
        raise ValueError(f'Endereço de email {email_addr} inválido!')
    return find_in(_users, lambda user: user.email_addr == email_addr)



def authenticate_user_by_email(email_addr: str, password: str) -> User | None:
    if not is_valid_email(email_addr):
        raise ValueError(f'Endereço de email {email_addr} inválido!')
    if user := get_user_by_email(email_addr):
        if hash_password(password) == user.password:
            return user
        return None 




def password_matches(user: User, password: str) -> bool:
    return user.password == hash_password(password)





def get_testimonials(count: int) -> List[Testimonial]:
    return [
        Testimonial(
            id = 1,
            name = 'Francisco Mendonça',
            user_occupation = 'CEO & Fundador',
            text = 'Quidem odit voluptate, obcaecati, explicabo nobis corporis perspiciatis nihil',
        ),
        Testimonial(
            id = 2,
            name = 'Sara Albuquerque',
            occupation = 'Designer',
            text = 'Export tempor illum tamen malis malis eram quae irure esse labore quem cillum quid',
        ),
        Testimonial(
            id = 3,
            name = 'Ana Silva',
            user_occupation = 'Store Owner',
            text = 'Enim nisi quem export duis labore cillum quae magna enim sint quorum nulla quem ver',
        ),
        Testimonial(
            id = 4,
            name = 'Fabio Rodrigues',
            user_occupation = 'Freelancer',
            text = 'Fugiat enim eram quae cillum dolore dolor amet nulla culpa multos export minim fug',
        ),
        Testimonial(
            id = 5,
            name = 'João Pedro Valez',
            user_occupation = 'Entrepreneur',
            text = 'Quis quorun aliqua sint quem legam fore sunt eram irure aliquaveniamtempornoste',
        ),
    ][:count]