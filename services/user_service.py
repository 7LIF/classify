__all__ = (
    'InvalidUserAttribute',
    'UserNotFound',
    'InvalidAuthentication',
    'user_count',
    'authenticate_user_by_email',
    'get_user_by_email',
    'get_user_by_id',
    'get_user_id_by_name',
    'get_user_by_external_id',
    'add_external_login',
    'password_matches',
    'DEFAULT_HASH_ALGO',
    'create_user_account',
    'add_profile_image_to_user',
    'update_user_account',
    'add_profile_image',
    'create_testimonial',
    'get_testimonials',
)


from typing import List
import aiofiles
from fastapi import UploadFile
import passlib.hash as passlib_hash
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload, aliased
from config_settings import conf
from common.common import coalesce, is_valid_email, find_first, is_valid_password #find_in
from data.database import database_session
from services import (
    item_service as iserv,
    user_service as userv,
    settings_service as setserv,
)
from data.models import (
    District,
    Favorite,
    User,
    Item,
    Testimonial,
    UserLoginData,
    UserAccountStatusEnum,
    UserAccount,
    HashAlgoEnum,
    ExternalProvider,
    UserLoginDataExternal,
)


#from datetime import date
#from random import randrange
#from typing import List
#from common.hash_password import hash_password
#from data.models import User, Testimonial

# variável que simula a base de dados - TEMPORARIAMENTE
#_users = []






USERS_IMAGES_URL = conf("USERS_IMAGES_URL")

IMAGE_CONTENT_TYPE_TO_EXTENSION = {
    'image/jpeg': 'jpg',
    'image/png': 'png',
    'image/gif': 'gif'
}

KNOWN_HASHERS = {
    HashAlgoEnum.PBKDF2_SHA256: passlib_hash.pbkdf2_sha256,
    HashAlgoEnum.PBKDF2_SHA512: passlib_hash.pbkdf2_sha512,
    HashAlgoEnum.ARGON2: passlib_hash.argon2,
}
DEFAULT_HASH_ALGO = HashAlgoEnum.PBKDF2_SHA512


class InvalidUserAttribute(ValueError):
    pass

class UserNotFound(Exception):
    pass

class InvalidAuthentication(Exception):
    pass



def user_count(
        concrete_type = UserAccount,
        db_session: Session | None = None,
) -> int:
    with database_session(db_session) as db_session:
        select_stm = select(func.count()).select_from(concrete_type)
        return db_session.execute(select_stm).scalar_one()
    
#### OU 
#def user_count(db_session: Session | None = None) -> int:
#    return userv.user_count(User, db_session)
###

def authenticate_user_by_email(
        email_addr: str,
        password: str,
        db_session: Session | None = None,
) -> UserAccount | None:
    with database_session(db_session) as db_session:
        if not is_valid_email(email_addr):
            raise UserNotFound(f'Invalid email address: {email_addr}')
        if user := get_user_by_email(email_addr, db_session):
            if password_matches(user, password):
                return user
        return None



def get_user_by_email(
        email_addr: str,
        db_session: Session | None = None,
) -> UserAccount | None:
    with database_session(db_session) as db_session:
        if not is_valid_email(email_addr):
            raise ValueError(f'Invalid email: {email_addr}')
        select_stmt = (
            select(UserAccount)
            .join(UserLoginData)
            .where(UserLoginData.email_addr == email_addr)
        )
        return db_session.execute(select_stmt).scalar_one_or_none()


def get_user_by_id(
        user_id: int,
        db_session: Session | None = None,
) -> UserAccount | None:
    with database_session(db_session) as db_session:
        UserAlias = aliased(User)
        select_stmt = (
            select(UserAccount)
            .join(UserAlias)
            .join(UserLoginData)
            .where(UserAccount.user_id == user_id)
        )
        return db_session.execute(select_stmt).scalar_one_or_none()




def get_user_actual_by_id(
        user_id: int,
        db_session: Session | None = None,
) -> User | None:
    with database_session(db_session) as db_session:
        select_stmt = (
            select(User)
            .where(User.user_id == user_id)
        )
        return db_session.execute(select_stmt).scalar_one_or_none()




def get_user_id_by_name(
    name: str, 
    db_session: Session | None = None,
) -> UserAccount | None:
    with database_session(db_session) as db_session:
        select_stmt = (
            select(UserAccount)
            .join(User)
            .join(UserLoginData)
            .where(UserAccount.name == name)
        )
        return db_session.execute(select_stmt).scalar_one_or_none()


def get_user_by_external_id(
        external_provider_id: int,
        external_user_id: str,
        db_session: Session | None = None,
) -> UserAccount | None:
    with database_session(db_session) as db_session:
        select_stmt = (
            select(UserAccount)
            .join(User)
            .join(UserLoginDataExternal)
            .join(ExternalProvider)
            .where(UserLoginDataExternal.external_user_id == external_user_id)
            .where(ExternalProvider.id == external_provider_id)
        )
        return db_session.execute(select_stmt).scalar_one_or_none()


def add_external_login(
        user: UserAccount,
        external_provider_id: int,
        external_user_id: str,
        db_session: Session | None = None,
) -> UserLoginDataExternal | None:
    with database_session(db_session) as db_session:
        if find_first(
                user.external_login_data,  
                external_provider_id, 
                key = lambda row: row.external_provider_id
        ):
            err_msg = f'User has already been registered with external provider {external_provider_id}'
            raise InvalidUserAttribute(err_msg)
        db_session.add(
            external_login_data := UserLoginDataExternal(
                user_id = user.user_id,
                external_provider_id = external_provider_id,
                external_user_id =  external_user_id,
            )
        )
        db_session.commit()
        db_session.refresh(external_login_data)
        return external_login_data


def password_matches(user: UserAccount, password: str) -> bool:
    hash_algo = user.user_login_data.hash_algo
    hasher = KNOWN_HASHERS[hash_algo]
    return hasher.verify(password, user.password_hash)


def hash_password(password: str, hash_algo: HashAlgoEnum = DEFAULT_HASH_ALGO) -> str:
    return KNOWN_HASHERS[hash_algo].hash(password)


def ensure_user_is(
        user_or_id: UserAccount | int,
        concrete_user_type: UserAccount,
        db_session: Session | None = None, 
) -> UserAccount:
    with database_session(db_session) as db_session:
        if isinstance(user_or_id, concrete_user_type):
            user =  user_or_id
        else:
            if not (user := get_user_by_id(user_or_id, db_session)):
                raise ValueError(f'Invalid id {id}.')

            if not isinstance(user, concrete_user_type):
                msg = (f'Invalid type for user {user.user_id}: expecting'
                    f'{concrete_user_type.__name__} but got {type(user).__name__}')
                raise TypeError(msg)
        return user









#def create_account(
#    name: str,
#    email_addr: str,
#    password: str,
#):
#    user = User(
#        randrange(10_000, 100_000),  # id
#        name,
#        email_addr,
#        hash_password(password),
#    )
#    _users.append(user)
#    return user
        




MAX_TESTIMONIALS = 10


#class InvalidFavorite(Exception):
#    pass


#class AlreadyFavorite(InvalidFavorite):
#    pass



def create_user_account(
        name: str,
        email_addr: str,
        password: str,
        phone_number: str | None = None,  
        address_line: str | None = None,
        zip_code: str | None = None,
        district_id: str | None = None,
        status: UserAccountStatusEnum = UserAccountStatusEnum.Active,
        db_session: Session | None = None,
) -> User:
    with database_session(db_session) as db_session:
        if get_user_by_email(email_addr, db_session):
            raise InvalidUserAttribute(f'Email already {email_addr} registered')

        db_session.add(
            user := User(
                type = User.__name__,
                name = name,
                phone_number = phone_number,
                address_line = address_line,
                zip_code = zip_code,
                district_id = district_id,
            )
        )
        user.status = status
        db_session.flush()
        
        db_session.add(
            UserLoginData(
                user_id = user.user_id,
                email_addr = email_addr,
                password_hash = userv.hash_password(password),
                hash_algo_id = userv.DEFAULT_HASH_ALGO.id,
            )
        )
        db_session.commit()
        db_session.refresh(user)
        return user



def add_profile_image_to_user(
    user_id: int, 
    profile_image: str, 
    db_session: Session | None = None
) -> User:
    with database_session(db_session) as db_session:
        user = db_session.query(User).get(user_id)
        if not user:
            raise InvalidUserAttribute(f'User with id {user_id} does not exist')

        user.profile_image = profile_image
        
        db_session.commit()
        db_session.refresh(user)
        return user




async def add_profile_image(
        user_or_id: UserAccount | int, 
        image_async_file: UploadFile,
        db_session: Session | None = None
) -> UserAccount:
    with database_session(db_session) as db_session:
        user = ensure_user_is(user_or_id, UserAccount, db_session)

        image_data = await image_async_file.read()
        user.profile_image = image_data
        db_session.commit()
        db_session.refresh(user)
        return user





def update_user_account(
        user_or_id: int | User,
        current_password: str | None = None,
        new_name: str | None = None,
        new_phone_number: str |None = None,
        new_email: str | None = None,
        new_password: str | None = None,
        new_address_line: str | None = None,
        new_zip_code: str | None = None,
        new_district_id: int | None = None,
        db_session: Session | None = None,
) -> User:
    with database_session(db_session) as db_session:
        user = ensure_user(user_or_id, db_session)

        #if not password_matches(user, current_password):
        #    raise ValueError(f"Password doesn't match.")

        if new_email:
            #if get_user_by_email(new_email, db_session):
                #raise InvalidUserAttribute(f'Email already {new_email} registered')
            user.email_addr = new_email

        if new_password:
            if not is_valid_password(new_password):
                raise InvalidUserAttribute(
                    f'Invalid new password for user {user.user_id}'
                )
            user.password_hash = userv.hash_password(new_password)

        user.name = coalesce(new_name, user.name)
        user.phone_number =  coalesce(new_phone_number, user.phone_number)
        user.address_line = coalesce(new_address_line, user.address_line)
        user.zip_code = coalesce(new_zip_code, user.zip_code)
        user.district_id = coalesce(new_district_id, user.district_id)
        

        db_session.commit()
        db_session.refresh(user)
        return user
    
    
    
    
    
    
    


def ensure_user(
        user_or_id: User | int,
        db_session: Session | None = None, 
) -> User:
    user = userv.ensure_user_is(user_or_id, User, db_session)
    assert isinstance(user, User)
    return user









def create_testimonial(
        user_id: int,
        user_occupation: str,
        text: str,
        image_url: str,
        db_session: Session | None = None,
) -> Testimonial:
    with database_session(db_session) as db_session:
        db_session.add(
            test := Testimonial(
                user_id = user_id,
                user_occupation = user_occupation,
                text = text,
                image_url = image_url,
            )
        )
        db_session.commit()
        db_session.refresh(test)
        return test


def get_testimonials(
        count: int = 0,
        db_session: Session | None = None,
) -> list[Testimonial]:
    with database_session(db_session) as db_session:
        select_stmt = select(Testimonial)
        scalar_results = db_session.execute(select_stmt).scalars()
        return scalar_results.fetchmany(count) if count > 0 else scalar_results.all()


#def is_favorite_item(
#        user: User,
#        item: Item,
#        db_session: Session | None = None,
#) -> bool:
#    with database_session(db_session) as db_session:
#        select_stmt = (
#            select(Favorite)
#            .where(Favorite.user_id == user.user_id)
#            .where(Favorite.item_id == item.id)
#        )
#        return bool(db_session.execute(select_stmt).scalar_one_or_none())


#def favorite_in_item(
#        user: User,
#        item: Item,
#        db_session: Session | None = None,
#) -> Favorite:
#    with database_session(db_session) as db_session:
#        if is_favorite_item(user, item, db_session):
#            raise AlreadyFavorite('item {item.id} already is favorite')
        

#        favorite = Favorite()
#        favorite.item = item
#        user.item.append(favorite)
#        db_session.add(favorite)
#        db_session.commit()
#        return favorite


def list_user_item (
    user_id: int, 
    db_session: Session | None = None,
) -> list[Item] | None:
    with database_session(db_session) as db_session:
        select_stmt = select(Item).where(Item.user_id == user_id)
        return db_session.execute(select_stmt).scalars().all()
    
def add_favorite_item_to_user(
    user_id: int,
    item_id: int,  
    db_session: Session | None = None,
) -> None:
    with database_session(db_session) as db_session:
        user = db_session.query(User).get(user_id)
        item = db_session.query(Item).get(item_id)

        if user and item:
            favorite = Favorite(item=item, user=user)
            db_session.add(favorite)
            db_session.commit()

def has_item_as_favorite(
 user_id: int,
    item_id: int,  
    db_session: Session | None = None,
) -> bool:
    
    with database_session(db_session) as db_session:
        favorite = (
                db_session.query(Favorite)
                .filter_by(user_id=user_id, item_id=item_id)
                .first()
            )
        return favorite is not None
    
def remove_favorite_item_from_user(
    user_id: int,
    item_id: int,
    db_session: Session | None = None,
) -> None:
    with database_session(db_session) as db_session:
        favorite = db_session.query(Favorite).filter_by(user_id=user_id, item_id=item_id).first()

        if favorite:
            db_session.delete(favorite)
            db_session.commit()

def user_has_favorite(
        user_id: int, 
        item_id: int, 
        db_session: Session | None = None
        ) -> bool:
    with database_session(db_session) as db_session:
        favorite = db_session.query(Favorite).filter_by(user_id=user_id, item_id=item_id).first()
        return favorite is not None

def get_user_favorites_ids(
        user_id: int, 
        db_session: Session | None = None
        ) -> List[Item]:
    with database_session(db_session) as db_session:
        favorites = db_session.query(Favorite). \
            filter_by(user_id=user_id). \
            options(joinedload(Favorite.item)). \
            all()

        return [favorite.item.id for favorite in favorites]

def get_user_favorites(
        user_id: int, 
        db_session: Session | None = None
        ) -> List[Item]:
    with database_session(db_session) as db_session:
        favorites = db_session.query(Favorite). \
            filter_by(user_id=user_id). \
            options(joinedload(Favorite.item)). \
            all()

        return [favorite.item for favorite in favorites]