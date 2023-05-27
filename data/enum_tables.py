import enum
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_mixin, declared_attr, Session
from data.model_base import SqlAlchemyBase


__all__ = (
    'EmailAddrStatus',
    'EmailAddrStatusEnum',
    'EmailAddrStatusMixin',
    'HashAlgo',
    'HashAlgoEnum',
    'HashAlgoMixin',
    'UserAccountStatus',
    'UserAccountStatusEnum',
    'UserAccountStatusMixin',
    'ItemStatus',
    'ItemStatusEnum',
    'ItemStatusMixin',
    'populate_enum_tables',
)


class EmailAddrStatusEnum(enum.Enum):
    Unconfirmed = (1, "Email address is yet to be validated")
    Confirmed = (2, "Email address was confirmed through an established process of email validation")

    @property
    def id(self) -> int:
        return self.value[0]

    @property
    def description(self) -> str:
        return self.value[1]

class EmailAddrStatus(SqlAlchemyBase):
    __tablename__ = 'EmailAddrStatus'

    id = Column(Integer, primary_key = True)
    name = Column(String(20), unique = True, nullable = False)
    description = Column(String(100), nullable = False)

    user_login_data_collection = relationship('UserLoginData', back_populates='_email_addr_status')

@declarative_mixin
class EmailAddrStatusMixin:
    @declared_attr
    def email_addr_status_id(cls):
        return Column(
            Integer, 
            ForeignKey('EmailAddrStatus.id'),
            nullable = False,
            server_default = f'{ EmailAddrStatusEnum.Unconfirmed.id }'
        )

    @property
    def email_addr_status(self) -> EmailAddrStatusEnum:
        return EmailAddrStatusEnum[self._email_addr_status.name]

    @email_addr_status.setter
    def email_addr_status(self, new_email_addr_status: EmailAddrStatusEnum):
        self.email_addr_status_id = new_email_addr_status.id    

    @declared_attr
    def _email_addr_status(cls):
        return relationship('EmailAddrStatus', back_populates = 'user_login_data_collection', lazy = 'immediate')

class HashAlgoEnum(enum.Enum):
    ARGON2 = (1, "Argon2 is a state of the art memory-hard password hash, and the winner of the 2013 Password Hashing Competition. Is intended to replace pbkdf2_sha256, bcrypt, and scrypt.")
    PBKDF2_SHA256 = (2, "Pure Python implementation of the PBKDF2-HMAC-SHA256 Password Storage Scheme provides a mechanism for encoding user passwords using the PBKDF2-HMAC-SHA256 message digest algorithm")
    PBKDF2_SHA512 = (3, "Pure Python implementation of the PBKDF2-HMAC-SHA512 Password Storage Scheme provides a mechanism for encoding user passwords using the PBKDF2-HMAC-SHA256 message digest algorithm")

    @property
    def id(self) -> int:
        return self.value[0]

    @property
    def description(self) -> str:
        return self.value[1]

class HashAlgo(SqlAlchemyBase):
    __tablename__ = 'HashAlgo'

    id = Column(Integer, primary_key = True)
    name = Column(String(20), unique = True, nullable = False)
    description = Column(String(100), nullable = False)

    user_login_data_collection = relationship('UserLoginData', back_populates='_hash_algo')

@declarative_mixin
class HashAlgoMixin:
    @declared_attr
    def hash_algo_id(cls):
        return Column(
            Integer, 
            ForeignKey('HashAlgo.id'),
            nullable = False,
            server_default = f'{ HashAlgoEnum.ARGON2.id }'
        )

    @property
    def hash_algo(self) -> HashAlgoEnum:
        return HashAlgoEnum[self._hash_algo.name]

    @hash_algo.setter
    def hash_algo(self, new_hash_algo: HashAlgoEnum):
        self.hash_algo_id = new_hash_algo.id    

    @declared_attr
    def _hash_algo(cls):
        return relationship('HashAlgo', back_populates = 'user_login_data_collection', lazy = 'immediate')



class UserAccountStatusEnum(enum.Enum):
    Active = (1, "User account is active")
    Blocked = (2, "User account was blocked due to security concerns")
    Inactive = (3, "User account was inactivated. User will have to change password")

    @property
    def id(self) -> int:
        return self.value[0]

    @property
    def description(self) -> str:
        return self.value[1]

class UserAccountStatus(SqlAlchemyBase):
    __tablename__ = 'UserAccountStatus'

    id = Column(Integer, primary_key = True)
    name = Column(String(20), unique = True, nullable = False)
    description = Column(String(100), nullable = False)

    user_account_collection = relationship('UserAccount', back_populates='_status')

@declarative_mixin
class UserAccountStatusMixin:
    @declared_attr
    def status_id(cls):
        return Column(
            Integer, 
            ForeignKey('UserAccountStatus.id'),
            nullable = False,
            server_default = f'{ UserAccountStatusEnum.Active.id }'
        )

    @property
    def status(self) -> UserAccountStatusEnum:
        return UserAccountStatusEnum[self._status.name]

    @status.setter
    def status(self, new_status: UserAccountStatusEnum):
        self.status_id = new_status.id    

    @declared_attr
    def _status(cls):
        return relationship('UserAccountStatus', back_populates = 'user_account_collection', lazy = 'immediate')

class ItemStatusEnum(enum.Enum):
    Active = (1, "Item is open for enrollments")
    Inactive = (2, "Item is inactive for any given reason")
    Retired = (3, "Item has been retired because it's no longer relevant")

    @property
    def id(self) -> int:
        return self.value[0]

    @property
    def description(self) -> str:
        return self.value[1]

class ItemStatus(SqlAlchemyBase):
    __tablename__ = 'ItemStatus'

    id = Column(Integer, primary_key = True)
    name = Column(String(20), unique = True, nullable = False)
    description = Column(String(100), nullable = False)

    item_collection = relationship('Item', back_populates='_status')

@declarative_mixin
class ItemStatusMixin:
    @declared_attr
    def status_id(cls):
        return Column(
            Integer, 
            ForeignKey('ItemStatus.id'),
            nullable = False,
            server_default = f'{ ItemStatusEnum.Active.id }'
        )

    @property
    def status(self) -> ItemStatusEnum:
        return ItemStatusEnum[self._status.name]

    @status.setter
    def status(self, new_status: ItemStatusEnum):
        self.status_id = new_status.id    

    @declared_attr
    def _status(cls):
        return relationship('ItemStatus', back_populates = 'item_collection', lazy = 'immediate')

def populate_enum_tables(db_session: Session):
    enums_and_tables = (
        (EmailAddrStatusEnum, EmailAddrStatus),
        (HashAlgoEnum, HashAlgo),
        (UserAccountStatusEnum, UserAccountStatus),
        (ItemStatusEnum, ItemStatus),
    )
    for enum_type, table in enums_and_tables:
        for enum in enum_type:
            row = table(id = enum.id, name = enum.name, description = enum.description) 
            db_session.add(row)
    db_session.commit()
