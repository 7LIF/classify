import sys
import os
sys.path[0] = f'{os.getcwd()}/..'

from typing import Callable, Iterable
from decimal import Decimal as dec
from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import Session
from data.database import *
from data.database_provider import *
from data.models import *
from services.user_service import *
from services.item_service import *
from services.settings_service import *
from data.models import District
from views.account import districts_viewmodel_info


db_session: Session | None = None


def main():
    from docopt import docopt 
    global db_session

    doc = f"""
        Create the datamodel for the classify's DB. By default, this script 
        also populates the DB with dummy values for testing. This module also 
        provides utilities to help test DB code during development.

        Usage:
            {sys.argv[0]} [-c | -i] [-s]

        Options:
            -c, --create-ddl-only        Create the data model ONLY. Don't populate it
                                        with any data
            -i, --initial-metadata-only  Create the data model and populate it ONLY with 
                                        initial metadata, like status values and 
                                        descriptions.
            -s, --leave-session-open     Don't explicitly close session before exiting.
        """
    args = docopt(doc)
    try:
        db_init(
            db_provider = SQLite(database = "classify.db"),
            create_datamodel = True,
            populate_metadata = not args['--create-ddl-only'],
        )
        db_session = get_db_session()

        if not (args['--create-ddl-only'] or args['--initial-metadata-only']):
            populate_database()
    finally:
        if not args['--leave-session-open']:
            db_session.close()


def populate_database():
    insert_external_auth_providers()
    insert_districts()
    insert_users()
    insert_external_logins()
    insert_testimonials()
    insert_categories()
    insert_subcategories()
    insert_items()


############################################################################
##      EXTERNAL AUTH PROVIDERS
############################################################################

def insert_external_auth_providers():
    insert_rows(
        label = 'EXTERNAL AUTH PROVIDERS',
        summary = lambda eap : f"Created external auth provider {eap.name} ('{eap.id}')",
        insert_function = accept_external_auth_provider,
        rows = (
            {
                'name': 'Google',
                'end_point_url': 'https://accounts.google.com/o/oauth2/auth',
                # 'end_point_url': 'https://accounts.google.com/.well-known/openid-configuration',
            },
            {
                'name': 'Microsoft',
                'end_point_url': 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize',
                # 'end_point_url': 'https://login.microsoftonline.com/.well-known/openid-configuration',
            }
        )
    )


############################################################################
##      Districts
############################################################################

# data source: http://centraldedados.pt/codigos_postais/

def insert_districts():
    insert_rows(
        label = 'DISTRICTS',
        summary = lambda distr: f"Created district '{distr.name}'",
        insert_function = accept_district,
        rows = (
            {
                'name': 'Aveiro',
                'image_url': 'aveiro.jpg'
            },
            {
                'name': 'Beja',
                'image_url': 'beja.jpg'
            },
            {
                'name': 'Braga',
                'image_url': 'braga.jpg'
            },
            {
                'name': 'Bragança',
                'image_url': 'braganca.jpg'
            },
            {
                'name': 'Castelo Branco',
                'image_url': 'castelo_branco.jpg'
            },
            {
                'name': 'Coimbra',
                'image_url': 'coimbra.jpg'
            },
            {
                'name': 'Évora',
                'image_url': 'evora.jpg'
            },
            {
                'name': 'Faro',
                'image_url': 'faro.jpg'
            },
            {
                'name': 'Guarda',
                'image_url': 'guarda.jpg'
            },
            {
                'name': 'Leiria',
                'image_url': 'leiria.jpg'
            },
            {
                'name': 'Lisboa',
                'image_url': 'lisboa.jpg'
            },
            {
                'name': 'Portalegre',
                'image_url': 'portalegre.jpg'
            },
            {
                'name': 'Porto',
                'image_url': 'porto.jpg'
            },
            {
                'name': 'Santarém',
                'image_url': 'santarem.jpg'
            },
            {
                'name': 'Setúbal',
                'image_url': 'setubal.jpg'
            },
            {
                'name': 'Viana do Castelo',
                'image_url': 'viana_castelo.jpg'
            },
            {
                'name': 'Vila Real',
                'image_url': 'vila_real.jpg'
            },
            {
                'name': 'Viseu',
                'image_url': 'viseu.jpg'
            },
            {
                'name': 'Ilha da Madeira',
                'image_url': 'ilha_madeira.jpg'
            },
            {
                'name': 'Ilha de Porto Santo',
                'image_url': 'ilha_porto_santo.jpg'
            },
            {
                'name': 'Ilha de Santa Maria',
                'image_url': 'ilha_santa_maria.jpg'
            },
            {
                'name': 'Ilha de São Miguel',
                'image_url': 'ilha_sao_miguel.jpg'
            },
            {
                'name': 'Ilha Terceira',
                'image_url': 'ilha_terceira.jpg'
            },
            {
                'name': 'Ilha da Graciosa',
                'image_url': 'ilha_graciosa.jpg'
            },
            {
                'name': 'Ilha de São Jorge',
                'image_url': 'ilha_sao_jorge.jpg'
            },
            {
                'name': 'Ilha do Pico',
                'image_url': 'ilha_pico.jpg'
            },
            {
                'name': 'Ilha do Faial',
                'image_url': 'ilha_faial.jpg'
            },
            {
                'name': 'Ilha das Flores',
                'image_url': 'ilha_flores.jpg'
            },
            {
                'name': 'Ilha do Corvo',
                'image_url': 'ilha_corvo.jpg'
            },
        )
    )
    










############################################################################
##
##      users
##
############################################################################

def insert_users():
    insert_rows(
        label = 'USERS',
        summary = lambda user: f"Created user '{user.name}' (id: {user.user_id})",
        insert_function = create_user_account,
        rows = (
            {
                'name': 'Augusto Andrade',
                'email_addr': 'augusto.andrade.aug@gmail.com',
                'password': 'abc',
                'address_line': 'Rua Pimenta da Cruz, Lote 33 - 1o Esquerdo',
                'zip_code': '2200-033 Águeda',
            },
            {
                'name': 'Avelino Américo',
                'email_addr': 'ave@mail.com',
                'password': 'abc',
                'address_line': 'Av. Da Esperança, Lote 21 - 4o Direito',
                'zip_code': '1010-100 Amarante',
            },
            {
                'name': 'Beatriz Batista',
                'email_addr': 'beatrizbatista@hotmail.com',
                'password': 'abc123',
                'address_line': 'Rua das Flores, Lote 14 - 2o Esquerdo',
                'zip_code': '2750-327 Cascais',
            },
            {
                'name': 'Carlos Carvalho',
                'email_addr': 'carlosc@gmail.com',
                'password': '123abc',
                'address_line': 'Av. da Liberdade, Lote 81 - 3o Direito',
                'zip_code': '1250-100 Lisboa',
            },
            {
                'name': 'Diego Domingues',
                'email_addr': 'diegodomingues13@mail.com',
                'password': 'a1b2c3',
                'address_line': 'Rua do Sol, Lote 6 - 4o Esquerdo',
                'zip_code': '4000-392 Porto',
            },
            {
                'name': 'Eva Esteves',
                'email_addr': 'evinha.e@mail.com',
                'password': 'p4ssword',
                'address_line': 'Rua dos Moinhos, Lote 9 - 1o Direito',
                'zip_code': '4900-341 Viana do Castelo',
            },
            {
                'name': 'Fábio Fernandes',
                'email_addr': 'fabiof13@mail.com',
                'password': 'qwerty',
                'address_line': 'Rua Nova, Lote 19 - 2o Esquerdo',
                'zip_code': '8000-020 Faro',
            },
            {
                'name': 'Gabriela Gomes',
                'email_addr': 'gabi_gomes_22@hotmail.com',
                'password': 'gabi123',
                'address_line': 'Av. da Praia, Lote 8 - 1o Esquerdo',
                'zip_code': '2520-038 Peniche',
            },           
        ),
    )


############################################################################
##
##      EXTERNAL LOGINS
##
############################################################################

def insert_external_logins():
        insert_rows(
        label = 'EXTERNAL LOGINS',
        summary = lambda data: (f"Added external user id '{data.external_user_id}' for student '{data.user_id}'"),
        insert_function = add_external_login,
        rows = (
            {
                'user': user('Augusto Andrade'),
                'external_provider_id': external_provider('Google').id,
                'external_user_id': '108481805106399484676',
            },
        )
    )


############################################################################
##
##      TESTIMONIALS
##
############################################################################

def insert_testimonials():
    insert_rows(
        label = 'TESTIMONIALS',
        summary = lambda test: f"Created '{test.user_name}' testimonial ",
        insert_function = create_testimonial,
        rows = (
            {
                'user_id': user('Augusto Andrade').user_id,
                'user_occupation': 'CEO & Founder',
                'text': 'Quidem odit voluptate, obcaecati, explicabo nobis corporis perspiciatis nihil doloremque eius omnis officia voluptates, facere saepe quas consequatur aliquam unde. Ab numquam reiciendis sequi.',
                'image_url': '201.jpg',
            },
            {
                'user_id': user('Avelino Américo').user_id,
                'user_occupation': 'Designer',
                'text': 'Export tempor illum tamen malis malis eram quae irure esse labore quem cillum quid cillum eram malis quorum velit fore eram velit sunt aliqua noster fugiat irure amet legam anim culpa.',
                'image_url': '202.jpg',
            },
            {
                'user_id': user('Fábio Fernandes').user_id,
                'user_occupation': 'Store Owner',
                'text': 'Enim nisi quem export duis labore cillum quae magna enim sint quorum nulla quem veniam duis minim tempor labore quem eram duis noster aute amet eram fore quis sint minim.',
                'image_url': '203.jpg',
            },
            {
                'user_id': user('Eva Esteves').user_id,
                'user_occupation': 'Entrepreneur',
                'text': 'Quis quorum aliqua sint quem legam fore sunt eram irure aliqua veniam tempor noster veniam enim culpa labore duis sunt culpa nulla illum cillum fugiat legam esse veniam culpa fore nisi cillum quid.',
                'image_url': '205.jpg',
            },
        )
    )


############################################################################
##
##      Categories
##
############################################################################

def insert_categories():
    insert_rows(
        label = 'CATEGORIES',
        summary = lambda cat: f"Created category '{cat.name}' (id: '{cat.id}')",
        insert_function = create_category,
        rows = (
            {
                'name': 'Veículos',
                'description': 'Carros, motas, veículos elétricos',
                'image_url': 'car.svg',
            },
            {
                'name': 'Eletrónicos',
                'description': '',
                'image_url': 'laptop.svg',
            },
            {
                'name': 'Mobiliário',
                'description': '',
                'image_url': 'furniture.svg',
            },
            {
                'name': 'Vestuário',
                'description': '',
                'image_url': 'tshirt.svg',
            },
            {
                'name': 'Acessórios',
                'description': '',
                'image_url': 'watch.svg',
            },
            {
                'name': 'Saúde & Beleza',
                'description': '',
                'image_url': 'hospital.svg',
            },
            {
                'name': 'Livros',
                'description': '',
                'image_url': 'education.svg',
            },
            {
                'name': 'Jogos',
                'description': '',
                'image_url': 'controller.svg',
            },
            {
                'name': 'Habitação',
                'description': '',
                'image_url': 'real-estate.svg',
            },
            {
                'name': 'Empregos',
                'description': '',
                'image_url': 'jobs.svg',
            },
            {
                'name': 'Outros',
                'description': '',
                'image_url': 'matrimony.svg',
            },
        )
    )



############################################################################
##
##      Subcategories
##
############################################################################

def insert_subcategories():
    insert_rows(
        label = 'SUBCATEGORIES',
        summary = lambda subcat: f"Created subcategory '{subcat.name}' (id: '{subcat.id}')",
        insert_function = create_subcategory,
        rows = (
            {
                'name': 'Carros',
                'description': 'Carros',
                'category_id': cat('Veículos').id,
            },
            {
                'name': 'Motociclos',
                'description': 'Motociclos',
                'category_id': cat('Veículos').id,
            },
            {
                'name': 'Veículos Elétricos',
                'description': 'Veículos Elétricos',
                'category_id': cat('Veículos').id,
            },
            {
                'name': 'Computadores Desktop',
                'description': 'Computadores Desktop, PC',
                'category_id': cat('Eletrónicos').id,
            },
            {
                'name': 'Portáteis',
                'description': 'Portáteis',
                'category_id': cat('Eletrónicos').id, 
            },
            {
                'name': 'Tablets',
                'description': 'Tablets',
                'category_id': cat('Eletrónicos').id,
            },
            {
                'name': 'Smartphones',
                'description': 'Smartphones, telemóveis',
                'category_id': cat('Eletrónicos').id,
            },
        )
    )
    
    




############################################################################
##
##      ITEMS
##
############################################################################

def insert_items():
    insert_rows(
        label = 'ITEMS',
        summary = lambda item: f"Created item '{item.title}' (id: '{item.id}')",
        insert_function = create_item,
        rows = (
            {
                'title': 'Apple Iphone X',
                'description':  'Smartphone Apple Iphone X',
                'main_image_url': 'item_id7_img_main.jpg',
                'image1_url': '',
                'image2_url': '',
                'image3_url': '',
                'image4_url': '',
                'price': dec(200.215).quantize(dec('0.01')),
                'address_line': '',
                'zip_code': '',
                'district_id': distr('Aveiro').id,
                'subcategory_id': subcat('Smartphones').id,
                'user_id': user('Augusto Andrade').user_id,
            },
            
            
            
            
            
        ),
    )


############################################################################
##
##      HELPER FUNCTIONS
##
############################################################################

def insert_rows(
        insert_function: Callable,
        label: str,
        rows: Iterable,
        summary: Callable | None = None,
):
    print()
    print(f"{label} _____________________________________________________")

    for row in rows:
        row['db_session'] = db_session
        obj = insert_function(**row)
        if summary:
            print(f"[+] {summary(obj)}")


def external_provider(name: str):
    return make_simple_query(ExternalProvider, ExternalProvider.name == name)


def user(name: str):
    return make_simple_query(User, User.name == name)

def distr(name: str):
    return make_simple_query(District, District.name == name)


def cat(name: str):
    return make_simple_query(Category, Category.name == name)


def subcat(name: str) -> Subcategory:
    return make_simple_query(Subcategory, Subcategory.name == name)


def item(title: str) -> Item:
    return make_simple_query(Item, Item.title == title)


def make_simple_query(table, query_fn):
    select_stmt = select(table).where(query_fn)
    return db_session.execute(select_stmt).scalar_one()


if __name__ == '__main__':
    main()