from decimal import Decimal as dec
from random import sample
from sqlalchemy import Float, select, or_, and_, func
from sqlalchemy.orm import Session
from data.database import database_session
from data.models import Category, Item, ItemStatusEnum, District, Subcategory


__all__ = (
    'item_count',
    'create_item',
    'most_popular_items',
    'available_items',
    'get_item_by_id',
    'get_district_name_from_item',
    'search_items',
)


MAX_ITEMS_SEARCH = 100


def item_count(db_session: Session | None = None) -> int:
    with database_session(db_session) as db_session:
        select_stm = select(func.count()).select_from(Item)
        return db_session.execute(select_stm).scalar_one()


def create_item(
        title: str,
        description: str,  
        main_image_url: str,
        image1_url: str,
        image2_url: str,
        image3_url: str,
        image4_url: str,
        address_line: str,
        zip_code: str,
        district_id: str,
        subcategory_id: str,
        price: dec,
        user_id: str,
        status: ItemStatusEnum = ItemStatusEnum.Active,
        db_session: Session | None = None,
) -> Item:
    with database_session(db_session) as db_session:
        db_session.add(
            item := Item(
                title = title,
                description = description,
                main_image_url = main_image_url,
                image1_url = image1_url,
                image2_url = image2_url,
                image3_url = image3_url,
                image4_url = image4_url,
                address_line = address_line,
                zip_code = zip_code,
                district_id = district_id,
                subcategory_id = subcategory_id,
                price = str(price),
                user_id = user_id,
            )
        )
        item.status = status
        db_session.commit()
        return item


def most_popular_items(
        count: int, 
        db_session: Session | None = None,
) -> list[Item]:
    with database_session() as db_session:
        items = available_items(db_session = db_session, count = 0)
        return sample(items, count) if len(items) >= count > 0 else items


def available_items(
        count: int = 0,
        db_session: Session | None = None,
) -> list[Item]:
    with database_session(db_session) as db_session:
        select_stmt = select(Item).where(Item.status_id == ItemStatusEnum.Active.id)
        if count > 0:
            select_stmt = select_stmt.limit(count)
        return db_session.execute(select_stmt).scalars().all()


def get_latest_items(
    count: int, 
    db_session: Session | None = None
) -> list[Item]:
    with database_session(db_session) as db_session:
        select_stmt = select(Item).where(Item.status_id == ItemStatusEnum.Active.id)
        select_stmt = select_stmt.order_by(Item.id.desc()).limit(count)
        return db_session.execute(select_stmt).scalars().all()


def get_random_items(
    count: int, 
    db_session: Session | None = None
) -> list[Item]:
    with database_session(db_session) as db_session:
        total_count = db_session.query(func.count(Item.id)).filter(Item.status_id == ItemStatusEnum.Active.id).scalar()
        select_stmt = select(Item).where(Item.status_id == ItemStatusEnum.Active.id)
        all_items = db_session.execute(select_stmt).scalars().all()
        random_items = sample(all_items, total_count)
        return random_items if total_count < count else random_items[:count]



def get_item_by_id(
    item_id: int, 
    db_session: Session | None = None,
) -> Item | None:
    with database_session(db_session) as db_session:
        select_stmt = select(Item).where(Item.id == item_id)
        return db_session.execute(select_stmt).scalar_one_or_none()




def get_district_name_from_item(
    item_id: int,
    session: Session | None = None, 
) -> str | None:
    item = session.query(Item).get(item_id)
    if item is not None:
        district = session.query(District).get(item.district_id)
        if district is not None:
            district_name = district.name
            return district_name
    return None

#def get_district_name_from_item(
#    item_id: int,
#    session: Session | None = None, 
#) -> str | None:
#    if session is None:
#        session = Session()
#    item = session.query(Item).get(item_id)
#    if item is not None:
#        user = item.user
#        district = user.district
#        return district.name
#    else:
#        return None



def search_item(
    keyword: str | None = None,
    category: str | None = None,
    district: str | None = None,
    price: str | None = None,
    db_session: Session | None = None
) -> list[Item] | None:
    with database_session(db_session) as db_session:
        
        query = db_session.query(Item).join(Subcategory).join(Category).join(District).filter(
            Item.status_id == ItemStatusEnum.Active.id
        )

        if keyword:
            query = query.filter(or_(Item.title.ilike(f'%{keyword}%'), Item.description.ilike(f'%{keyword}%')))
        if category and category != 'none':
            query = query.filter(Category.name == category)
        if district and district != 'none':
            query = query.filter(District.name == district)
        if price and price != 'none':
            query = query.filter(func.cast(Item.price, Float) <= float(price))
            
        return query.all()