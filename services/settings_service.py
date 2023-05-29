################################################################################
##      Importing necessary modules
################################################################################

from random import sample
from sqlalchemy import select
from sqlalchemy.orm import Session
from data.database import database_session
from data.enum_tables import ItemStatusEnum
from data.models import District, Category, Item, Subcategory, ExternalProvider


__all__ = (
    'accept_district',
    'get_accepted_district',
    'get_random_districts_with_items',
    'create_category',
    'get_accepted_category',
    'count_accepted_categories',
    'create_subcategory',
    'accept_external_auth_provider',
    'get_external_auth_providers',
    'get_external_provider_by_id',
    'get_external_provider_by_name',
)


def accept_district(
        name: str,
        image_url: str,
        db_session: Session | None = None,
) -> District:
    with database_session(db_session) as db_session:
        db_session.add(
            district := District(
                name = name,
                image_url = image_url,
            )
        )
        db_session.commit()
        return district


def get_accepted_district(
        db_session: Session | None = None,
) -> list[District]:
    with database_session(db_session) as db_session:
        select_stmt = select(District)
        return db_session.execute(select_stmt).scalars().all()
    
    
    
    
def get_random_districts_with_items(
    count: int, 
    db_session: Session | None = None
) -> list[District]:
    with database_session(db_session) as db_session:
        stmt = select(District).join(Item, Item.district_id == District.id).where(Item.status_id == ItemStatusEnum.Active.id)
        all_districts = db_session.execute(stmt).scalars().all()
        districts_with_items = [district for district in all_districts if district.items]
        if len(districts_with_items) <= count:
            return districts_with_items
        return sample(districts_with_items, count)






def create_category(
        name: str,
        description: str,
        image_url: str,
        db_session: Session | None = None,
) -> Category:
    with database_session(db_session) as db_session:
        db_session.add(
            cat := Category(
                name = name,
                description = description,
                image_url = image_url,
            )
        )
        db_session.commit()
        db_session.refresh(cat)
        return cat




def get_accepted_category(
        db_session: Session | None = None,
) -> list[Category]:
    with database_session(db_session) as db_session:
        select_stmt = select(Category)
        return db_session.execute(select_stmt).scalars().all()



def count_accepted_categories() -> int:
    accepted_categories = get_accepted_category()
    return len(accepted_categories)



def create_subcategory(
        name: str,
        description: str,
        category_id: int,
        db_session: Session | None = None,
) -> Subcategory:
    with database_session(db_session) as db_session:
        db_session.add(
            subcat := Subcategory(
                name = name,
                description = description,
                category_id = category_id,
            )
        )
        db_session.commit()
        db_session.refresh(subcat)
        return subcat


def accept_external_auth_provider(
        name: str,
        end_point_url: str,
        db_session: Session | None = None,
) -> District:
    with database_session(db_session) as db_session:
        db_session.add(
            eap := ExternalProvider(
                name = name,
                end_point_url = end_point_url,
            )
        )
        db_session.commit()
        db_session.refresh(eap)
        return eap


def get_external_auth_providers(
    db_session: Session | None = None,
) -> list[ExternalProvider]:
    with database_session(db_session) as db_session:
        select_stmt = select(ExternalProvider).where(ExternalProvider.active == True)
        return db_session.execute(select_stmt).scalars().all()


def get_external_provider_by_id(
    external_provider_id: int,
    db_session: Session | None = None,
) -> ExternalProvider | None:
    with database_session(db_session) as db_session:
        select_stmt = (
            select(ExternalProvider)
            .where(ExternalProvider.id == external_provider_id)
            .where(ExternalProvider.active == True)
        )
        return db_session.execute(select_stmt).scalar_one_or_none()


def get_external_provider_by_name(
    name: str,
    db_session: Session | None = None,
) -> ExternalProvider | None:
    with database_session(db_session) as db_session:
        select_stmt = (
            select(ExternalProvider)
            .where(ExternalProvider.name == name)
            .where(ExternalProvider.active == True)
        )
        return db_session.execute(select_stmt).scalar_one_or_none()
