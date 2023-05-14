################################################################################
##      Importing necessary modules
################################################################################

from datetime import date, datetime
from decimal import Decimal as dec
from dataclasses import dataclass, field
from services import user_service


@dataclass
class Category:
    id: int
    category_name: str
    icon: str
    weblink: str
    count_items_category: int


@dataclass
class Subcategory:
    id: int
    subcategory_name: str
    category_name: str
    count_items_category: int
    
    
@dataclass
class District:
    id: int
    district_name: str


@dataclass
class Region:
    id: int
    region_name: str
    district_name: str



################################################################################
##      Defining the Item class with attributes
################################################################################  

@dataclass
class Item:
    id: int
    post_title: str
    subcategory: str
    category: str
    publication_date: str
    last_update: str
    price: dec
    price_type: str
    item_status: str
    weblink: str
    location_region: str
    location_district: str
    summary: str
    img_main: str
    img1: str
    img2: str
    img3: str
    img4: str
    user_id: int
    user_name: str
    profile_img_url: str
    premium: str



################################################################################
##      Defining the User class with attributes
################################################################################    
    
@dataclass
class User:
    id: int
    name: str
    email: str
    password: str
    birth_date: date | None = None
    presentation: str | None = None
    profile_img_url: str | None = None
    created_date: date = field(default_factory=date.today)
    last_login: datetime = field(default_factory=date.today)


################################################################################
##      Defining the Testimonial class with attributes
################################################################################  

@dataclass
class Testimonial:
    user_id: int
    user_name: str
    user_occupation: str
    text: str