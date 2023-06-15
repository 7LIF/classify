from sqlalchemy.orm import relationship, Session
from data.model_base import SqlAlchemyBase
from sqlalchemy import (
    CheckConstraint,
    Column,
    Boolean,
    Date,
    ForeignKey,
    Identity,
    Integer,
    String,
    DateTime,
    UniqueConstraint,
    func,
)


################################################################################
##      ENUM TABLES
##      NOTE: This module first needs to be generated/compiled.
################################################################################

from data.enum_tables import *


################################################################################
##      CONSTANTS
################################################################################

URL_SIZE = 300

EXTERNAL_PROVIDER_NAME_SIZE = 20
USER_EXTERNAL_ID_TOKEN_MAX_SIZE = 255

EMAIL_REGEXP = r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
NAME_REGEXP = r'^[^\W_0-9]{2,}(\s[^\W_0-9]{2,})+$'
NAME_SIZE = 100                         # FULLNAME
PHONE_NUMBER_SIZE = 9
ADDRESS_LINE_SIZE = 60
ZIP_CODE_SIZE = 10
PASSWORD_HASH_SIZE = 130

DISTRICT_NAME_MAX_SIZE = 25             # largest district name has 19 chars...
DISTRICT_NAME_MIN_SIZE = 3              # shortest district name has 4 chars...

TESTIMONIAL_TEXT_SIZE = 200

ITEM_TITLE_SIZE = 30
ITEM_DESC_SIZE = 1500

CATEGORY_NAME_SIZE = 30
CATEGORY_NAME_DESC = 100
CATEGORY_IMAGE_URL = 300


################################################################################
##      DATA MODEL: User/Login/Account Related Stuff
################################################################################

# NOTE: most of the parameters come from the server configuration (a Python file).
# This table contains only basic information about the provider

class ExternalProvider(SqlAlchemyBase):
    __tablename__ = 'ExternalProvider'

    id = Column(Integer, Identity(start = 1), primary_key = True)
    name = Column(String(EXTERNAL_PROVIDER_NAME_SIZE), unique = True, nullable = False)
    end_point_url = Column(String(URL_SIZE), unique = True, nullable = False)
    active = Column(Boolean, nullable = False, server_default = '1')

    users_using = relationship('UserLoginDataExternal', back_populates = 'external_provider')



class UserLoginDataExternal(SqlAlchemyBase):
    __tablename__ = 'UserLoginDataExternal'

    id = Column(Integer, Identity(start = 20000), primary_key = True)
    user_id = Column(Integer, ForeignKey('UserAccount.user_id'), nullable = False)
    external_provider_id = Column(Integer, ForeignKey('ExternalProvider.id'), nullable = False)
    external_user_id = Column(String(USER_EXTERNAL_ID_TOKEN_MAX_SIZE), unique = True, nullable = False)
    date_created =  Column(Date, nullable = False, server_default = func.current_date())

    external_provider = relationship('ExternalProvider', back_populates = 'users_using')
    user_account = relationship('UserAccount', back_populates = 'external_login_data')

    UniqueConstraint('user_id', 'external_provider_id', name = 'UserExternalProviderIDX')



# adding the extra field(s) to the superclass, and not just creating a subclass that extends the superclass.
# So we don't need the subclass name
class _(HashAlgo):
    date = Column(Date, nullable = False, server_default = func.current_date())



class UserLoginData(SqlAlchemyBase, EmailAddrStatusMixin, HashAlgoMixin):
    __tablename__ = 'UserLoginData'
    
    user_id = Column(Integer, ForeignKey('UserAccount.user_id'), primary_key = True)
    password_hash = Column(String(PASSWORD_HASH_SIZE), nullable = False)
    email_addr = Column(String, unique = True, nullable = False)
    last_login = Column(DateTime)

    user_account = relationship('UserAccount', back_populates = 'user_login_data')

    @property
    def name(self) -> str:
        return self.user_account.name
    
    __table_args__ = (
        CheckConstraint(
            f'email_addr REGEXP "{EMAIL_REGEXP}"', 
            name = 'EmailCK'
        ),
    )


class District(SqlAlchemyBase):
    __tablename__ = 'District'

    id = Column(Integer, Identity(always = True, start = 1), primary_key = True)
    name = Column(String(DISTRICT_NAME_MAX_SIZE), nullable = False, unique = True)
    image_url = Column(String(URL_SIZE), unique = True, nullable = False)
    
    user_accounts = relationship('UserAccount', back_populates = 'district')
    items = relationship('Item', back_populates = 'district')



class UserAccount(SqlAlchemyBase, UserAccountStatusMixin):
    __tablename__ = 'UserAccount'

    user_id = Column(Integer, Identity(always = True, start = 1), primary_key = True)
    type = Column(String(50))
    name = Column(String(NAME_SIZE), nullable = False)
    phone_number = Column(String(PHONE_NUMBER_SIZE))
    address_line = Column(String(ADDRESS_LINE_SIZE))
    zip_code = Column(String(ZIP_CODE_SIZE))
    district_id = Column(Integer, ForeignKey('District.id'))
    date_created =  Column(Date, nullable = False, server_default = func.current_date())

    @property
    def firstname(self) -> str:
        return self.name.partition(' ')[0]

    @property
    def email_addr(self) -> str:
        return self.user_login_data.email_addr

    @email_addr.setter
    def email_addr(self, new_email_addr: str):
        self.user_login_data.email_addr = new_email_addr 

    @property
    def password_hash(self) -> str:
        return self.user_login_data.password_hash

    @password_hash.setter
    def password_hash(self, password_hash: str):
        self.user_login_data.password_hash = password_hash
    
    @property
    def district_name(self) -> str:
        if self.district:
           return self.district.name
        return ''
    

    # 'uselist = False' turns what was previously a one-to-many 
    # UserAccount.user_login_data relationship into a one-to-one
    user_login_data = relationship('UserLoginData', back_populates = 'user_account', uselist = False, lazy = 'immediate')
    external_login_data = relationship('UserLoginDataExternal', back_populates = 'user_account', lazy = 'immediate')
    district = relationship('District', back_populates = 'user_accounts', lazy = 'immediate')

    __table_args__ = (
        CheckConstraint(
            f'name REGEXP "{NAME_REGEXP}"', 
            name = 'NameCK'
        ),
    )

    __mapper_args__ = {
        'polymorphic_identity': 'UserAccount',
        'polymorphic_on': type,
    }


class User(UserAccount):
    __tablename__ = 'User'

    user_id = Column(Integer, ForeignKey("UserAccount.user_id"), primary_key = True)
    profile_image = Column(String(URL_SIZE), unique = True)
    favorites = relationship("Item")
    
    items = relationship('Item', back_populates = 'user')
    testimonials = relationship('Testimonial', back_populates = 'user')
    favorites = relationship("Favorite", back_populates="user", overlaps="favorite_items")
    favorite_items = relationship('Item', secondary='Favorite', back_populates='favorited_by', overlaps="favorites")

    __mapper_args__ = {
        'polymorphic_identity': 'User',
    }


class Testimonial(SqlAlchemyBase):
    __tablename__ = 'Testimonial'

    id = Column(Integer, primary_key = True, autoincrement = 'auto')
    text = Column(String(TESTIMONIAL_TEXT_SIZE), nullable = False)
    user_occupation = Column(String(50), nullable = False)
    date_created = Column(Date, nullable = False, server_default = func.current_date())
    user_id = Column(Integer, ForeignKey("User.user_id"), nullable = False, unique = True)
    image_url = Column(String(URL_SIZE), unique = True, nullable = False)

    @property
    def user_name(self) -> str:
        return self.user.name

    user = relationship('User', back_populates = 'testimonials', lazy = 'immediate',)



################################################################################
##      DATA MODEL: Item and Related Tables
################################################################################

class Category(SqlAlchemyBase):
    __tablename__ = 'Category'

    id = Column(Integer, Identity(start = 1), primary_key = True)
    name = Column(String(CATEGORY_NAME_SIZE), unique = True, nullable = False)
    description = Column(String(CATEGORY_NAME_DESC), nullable = True)
    image_url = Column(String(CATEGORY_IMAGE_URL), nullable = False)

    subcategories = relationship('Subcategory', back_populates = 'category')



class Subcategory(SqlAlchemyBase):
    __tablename__ = 'Subcategory'

    id = Column(Integer, Identity(start = 1), primary_key = True)
    name = Column(String(CATEGORY_NAME_SIZE), nullable = False)
    description = Column(String(CATEGORY_NAME_DESC), nullable = True)
    category_id = Column(Integer, ForeignKey("Category.id"), nullable = False)

    @property
    def category_name(self) -> str:
        return self.category.name
    
    category = relationship('Category', back_populates = 'subcategories', lazy = 'immediate')
    items = relationship('Item', back_populates = 'subcategory')
    
    UniqueConstraint('name', 'category_id', name = 'NameSubCatIDX')




class Item(SqlAlchemyBase, ItemStatusMixin):
    __tablename__ = 'Item'

    id = Column(Integer, Identity(start = 1), primary_key = True)
    title = Column(String(ITEM_TITLE_SIZE), nullable = False)
    description = Column(String(ITEM_DESC_SIZE), nullable = False)
    main_image_url = Column(String(URL_SIZE), nullable = False)
    image1_url = Column(String(URL_SIZE), nullable = True)
    image2_url = Column(String(URL_SIZE), nullable = True)
    image3_url = Column(String(URL_SIZE), nullable = True)
    image4_url = Column(String(URL_SIZE), nullable = True)
    address_line = Column(String(ADDRESS_LINE_SIZE), nullable = True)
    zip_code = Column(String(ZIP_CODE_SIZE), nullable = True)
    district_id = Column(Integer, ForeignKey('District.id'), nullable = False)
    date_created =  Column(Date, nullable = False, server_default = func.current_date())
    last_updated_date = Column(Date, nullable = False, server_default = func.current_date())
    price = Column(String(20), server_default='0.00', nullable = False)   # just for SQLite

    subcategory_id = Column(Integer, ForeignKey("Subcategory.id"),nullable = False,)
    user_id = Column(Integer, ForeignKey("User.user_id"), nullable = False,)

    @property
    def subcategory_name(self) -> str:
        return self.subcategory.name

    @property
    def category_name(self) -> str:
        return self.category.name
    
    @property
    def user_name(self) -> str:
        return self.user.name
    
    @property
    def user_profile_image(self) -> str:
        return self.user.profile_image
    
    @property
    def district_name(self) -> str:
        if self.district:
            return self.district.name
        return ''
    
    subcategory = relationship('Subcategory', back_populates = 'items', innerjoin = True, lazy = 'immediate',)
    user = relationship('User', back_populates = 'items', innerjoin = True, lazy = 'immediate',)
    district = relationship('District', back_populates = 'items', lazy = 'immediate')
    favorited_by = relationship('User', secondary='Favorite', back_populates='favorite_items', overlaps="favorites")
    
    __table_args__ = (
        CheckConstraint(
            f'price >= 0',
            name = 'PriceCK'
        ),
    )


class Favorite(SqlAlchemyBase):
    __tablename__ = 'Favorite'

    id = Column(Integer, Identity(start=1), primary_key=True)
    item_id = Column(Integer, ForeignKey("Item.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("User.user_id"), nullable=False)
    
    user = relationship('User', overlaps='favorite_items, favorited_by')
    item = relationship('Item', overlaps='favorite_items, favorited_by')
    
    __table_args__ = (
        UniqueConstraint('user_id', 'item_id'),
    )


################################################################################
##      METADATA: Populate tables with initial metadata
################################################################################

def populate_metadata(db_session: Session):
    populate_enum_tables(db_session)
