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
    insert_profile_image_to_user()
    insert_external_logins()
    insert_testimonials()
    insert_categories()
    insert_subcategories()
    insert_items()
    insert_msgs()


############################################################################
##      EXTERNAL AUTH PROVIDERS
############################################################################

def insert_external_auth_providers():
    insert_rows(
        label = 'EXTERNAL AUTH PROVIDERS',
        summary = lambda eap : f"Created external auth provider {eap.name} (id: {eap.id})",
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
        summary = lambda distr: f"Created district '{distr.name}' (id: {distr.id})",
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
##      Users Account
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
                'phone_number': 962135748,
                'address_line': 'Rua Pimenta da Cruz, Lote 33 - 1o Esquerdo',
                'zip_code': '2200-033 Águeda',
                'district_id': distr('Aveiro').id,
            },
            {
                'name': 'Avelino Américo',
                'email_addr': 'ave@mail.com',
                'password': 'abc',
                'phone_number': 913245434,
                'address_line': 'Av. Da Esperança, Lote 21 - 4o Direito',
                'zip_code': '1010-100 Amarante',
                'district_id': distr('Porto').id,
            },
            {
                'name': 'Beatriz Batista',
                'email_addr': 'beatrizbatista@hotmail.com',
                'password': 'abc123',
                'phone_number': 936546154,
                'address_line': 'Rua das Flores, Lote 14 - 2o Esquerdo',
                'zip_code': '2750-327 Cascais',
                'district_id': distr('Lisboa').id,
            },
            {
                'name': 'Carlos Carvalho',
                'email_addr': 'carlosc@gmail.com',
                'password': '123abc',
                'phone_number': 924687684,
                'address_line': 'Av. da Liberdade, Lote 81 - 3o Direito',
                'zip_code': '1250-100 Lisboa',
                'district_id': distr('Lisboa').id,
            },
            {
                'name': 'Diego Domingues',
                'email_addr': 'diegodomingues13@mail.com',
                'password': 'a1b2c3',
                'phone_number': 912106748,
                'address_line': 'Rua do Sol, Lote 6 - 4o Esquerdo',
                'zip_code': '4000-392 Porto',
                'district_id': distr('Porto').id,
            },
            {
                'name': 'Eva Esteves',
                'email_addr': 'evinha.e@mail.com',
                'password': 'p4ssword',
                'phone_number': 965687785,
                'address_line': 'Rua dos Moinhos, Lote 9 - 1o Direito',
                'zip_code': '4900-341 Viana do Castelo',
                'district_id': distr('Viana do Castelo').id,
            },
            {
                'name': 'Fábio Fernandes',
                'email_addr': 'fabiof13@mail.com',
                'password': 'qwerty',
                'phone_number': 916332345,
                'address_line': 'Rua Nova, Lote 19 - 2o Esquerdo',
                'zip_code': '8000-020 Faro',
                'district_id': distr('Faro').id,
            },
            {
                'name': 'Gabriela Gomes',
                'email_addr': 'gabi_gomes_22@hotmail.com',
                'password': 'gabi123',
                'phone_number': 926887545,
                'address_line': 'Av. da Praia, Lote 8 - 1o Esquerdo',
                'zip_code': '2520-038 Peniche',
                'district_id': distr('Leiria').id,
            },
            {
                'name': 'José Faria',
                'email_addr': 'faria.j@hotmail.com',
                'password': 'jonyquerty123',
                'phone_number': 915435043,
                'address_line': 'Rua da Carreira',
                'zip_code': '9000-036 Funchal',
                'district_id': distr('Ilha da Madeira').id,
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
        summary = lambda data: (f"Added external login '{data.external_user_id}' to the user id '{data.user_id}' (id: {data.id})"),
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
        summary = lambda test: f"Created '{test.user_name}' testimonial (id: {test.id})",
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
        summary = lambda cat: f"Created category '{cat.name}' (id: {cat.id})",
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
                'name': 'Livros',
                'description': '',
                'image_url': 'education.svg',
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
        summary = lambda subcat: f"Created subcategory '{subcat.name}' (id: {subcat.id})",
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
                'name': 'Carros Elétricos',
                'description': 'Veículos Elétricos',
                'category_id': cat('Veículos').id,
            },
            {
                'name': 'Computadores Desktop',
                'description': 'Computadores Desktop, PC',
                'category_id': cat('Eletrónicos').id,
            },
            {
                'name': 'Portáteis',
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
            {
                'name': 'Câmaras Fotográficas',
                'description': 'Câmaras Fotográficas',
                'category_id': cat('Eletrónicos').id,
            },
            {
                'name': 'Consolas de Jogos',
                'description': 'Consolas de Jogos',
                'category_id': cat('Eletrónicos').id,
            },
            {
                'name': 'Outros Eletrónicos',
                'description': 'Outros Eletrónicos',
                'category_id': cat('Eletrónicos').id,
            },
            {
                'name': 'Mobilia de Quarto',
                'description': 'Mobilia de Quarto',
                'category_id': cat('Mobiliário').id,
            },
            {
                'name': 'Mobilia de Sala',
                'description': 'Mobilia de Sala',
                'category_id': cat('Mobiliário').id, 
            },
            {
                'name': 'Mobilia de Cozinha',
                'description': 'Mobilia de Cozinha',
                'category_id': cat('Mobiliário').id,
            },
            {
                'name': 'Outro Mobiliário',
                'description': 'Mobiliário de Exterior',
                'category_id': cat('Mobiliário').id,
            },
            {
                'name': 'Vestuário de Mulher',
                'description': 'Vestuário de Mulher',
                'category_id': cat('Vestuário').id,
            },
            {
                'name': 'Vestuário de Homem',
                'description': 'Vestuário de Homem',
                'category_id': cat('Vestuário').id,
            },
            {
                'name': 'Vestuário de Criança & Bebé',
                'description': 'Vestuário de Criança & Bebé',
                'category_id': cat('Vestuário').id,
            },
            {
                'name': 'Relógios',
                'description': 'Relógios',
                'category_id': cat('Acessórios').id,
            },
            {
                'name': 'Malas',
                'description': 'Malas',
                'category_id': cat('Acessórios').id,
            },
            {
                'name': 'Outros Acessórios',
                'description': 'Outros Acessórios',
                'category_id': cat('Acessórios').id,
            },
            {
                'name': 'Livros Escolares',
                'description': 'Livros Escolares',
                'category_id': cat('Livros').id,
            },
            {
                'name': 'Livros em Português',
                'description': 'Livros Escolares',
                'category_id': cat('Livros').id,
            },
            {
                'name': 'Livros em Língua Estrangeira',
                'description': 'Livros Escolares',
                'category_id': cat('Livros').id,
            },
            {
                'name': 'Saúde & Beleza',
                'description': 'Saúde & Beleza',
                'category_id': cat('Outros').id,
            },
            {
                'name': 'Diversos',
                'description': 'Todos os artigos que não se enquadram em nenhuma das categorias anteriores',
                'category_id': cat('Outros').id,
            },
        )
    )
    


def insert_profile_image_to_user():
    insert_rows(
        label='ADD PROFILE IMAGE TO USER TABLE',
        summary = lambda user: f"Added profile image '{user.profile_image}' to the user id '{user.user_id}' (id: {user.user_id})",
        insert_function= add_profile_image_to_user,
        rows=(
            {
                'user_id': user('Augusto Andrade').user_id,
                'profile_image': 'profile_image1.jpg',
            },
            {
                'user_id': user('Avelino Américo').user_id,
                'profile_image': 'profile_image2.jpg',
            },
            {
                'user_id': user('Beatriz Batista').user_id,
                'profile_image': 'profile_image3.jpg',
            },
            {
                'user_id': user('Carlos Carvalho').user_id,
                'profile_image': 'profile_image4.jpg',
            },
            {
                'user_id': user('Diego Domingues').user_id,
                'profile_image': 'profile_image5.jpg',
            },
            {
                'user_id': user('Eva Esteves').user_id,
                'profile_image': 'profile_image6.jpg',
            },
            {
                'user_id': user('Fábio Fernandes').user_id,
                'profile_image': 'profile_image7.jpg',
            },
            {
                'user_id': user('Gabriela Gomes').user_id,
                'profile_image': 'profile_image8.jpg',
            },
            {
                'user_id': user('José Faria').user_id,
                'profile_image': 'profile_image9.jpg',
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
        summary = lambda item: f"Created item '{item.title}' (id: {item.id})",
        insert_function = create_item,
        rows = (
            {
                'title': 'MacBook Pro 13 polegadas',
                'description': 'Vendo MacBook Pro de 13 polegadas em excelente estado. Este MacBook Pro é equipado com um processador Intel Core i5 de 8ª geração, 8 GB de RAM e um SSD de 256 GB, é perfeito para trabalhos criativos, edição de fotos e vídeo. Tem teclado retroiluminado e trackpad com tecnologia Force Touch. Inclui sistema operacional macOS Big Sur mais recente e está pronto para ser usado imediatamente. Modelo: Apple MacBook Pro, Chip Apple M1 com CPU de 8 núcleos e GPU de 8 núcleos, 256GB SSD, 13.3 polegadas, 2560x1600. Este MacBook Pro é perfeito para profissionais que precisam de um laptop confiável e poderoso para trabalhar, estudar ou se divertir.',
                'main_image_url': 'item_id1_img_main.jpg',
                'image1_url': 'item_id1_img1.jpg',
                'image2_url': 'item_id1_img2.jpg',
                'image3_url': 'item_id1_img3.jpg',
                'image4_url': 'item_id1_img4.jpg',
                'price': dec(666.00).quantize(dec('0.01')),
                'address_line': 'Rua dos Moinhos',
                'zip_code': '4900-341 Viana do Castelo',
                'district_id': distr('Viana do Castelo').id,
                'subcategory_id': subcat('Portáteis').id,
                'user_id': user('Eva Esteves').user_id,
            },
            {
                'title': 'Cama King Size Espaçosa',
                'description': 'A cama king size oferece uma generosa área de descanso, permitindo que você se espalhe e desfrute de um espaço amplo e confortável. Comprimento: 2 metros; Largura: 1,8 metros; Estrutura robusta e durável para suporte sólido e estabilidade. Design elegante que se adapta perfeitamente a qualquer estilo de decoração. Qualidade excecional para garantir durabilidade e longevidade.',
                'main_image_url': 'item_id2_img_main.jpg',
                'image1_url': '',
                'image2_url': '',
                'image3_url': '',
                'image4_url': '',
                'price': dec(200.00).quantize(dec('0.01')),
                'address_line': 'Av. Da Esperança',
                'zip_code': '1010-100 Amarante',
                'district_id': distr('Porto').id,
                'subcategory_id': subcat('Mobilia de Quarto').id,
                'user_id': user('Avelino Américo').user_id,
            },
            {
                'title': 'Canon SX Powershot D-SLR',
                'description': 'A camera é equipada com um sensor de alta resolução e uma lente de alta qualidade, obtendo imagens nítidas e detalhadas. Possui um zoom ótico poderoso sem perder a qualidade. A estabilização avançada de imagem garante fotos e vídeos sem tremores, enquanto o modo manual permite um controle criativo completo.',
                'main_image_url': 'item_id3_img_main.jpg',
                'image1_url': '',
                'image2_url': '',
                'image3_url': '',
                'image4_url': '',
                'price': dec(200.00).quantize(dec('0.01')),
                'address_line': 'Rua das Flores',
                'zip_code': '2750-327 Cascais',
                'district_id': distr('Lisboa').id,
                'subcategory_id': subcat('Câmaras Fotográficas').id,
                'user_id': user('Beatriz Batista').user_id,
            },
            {
                'title': 'BMW 5 Series Gran Turismo 535i RWD',
                'description':  'BMW 5 Series Gran Turismo 535i RWD de 2012. Apenas teve 1 proprietário. Quilometragem: 149.413km; Tração: Tração traseira; Cor exterior: Azul; Cor interior: Bege; Motor: Motor de 3L I6 com 300 cavalos de potência; Consumo de combustível: 9.41 L/100km; Tipo de combustível: Gasolina; Transmissão: Automática de 8 velocidades.',
                'main_image_url': 'item_id4_img_main.jpeg',
                'image1_url': 'item_id4_img1.jpeg',
                'image2_url': 'item_id4_img2.jpeg',
                'image3_url': 'item_id4_img3.jpeg',
                'image4_url': '',
                'price': dec(7500.00).quantize(dec('0.01')),
                'address_line': '',
                'zip_code': '1250-100 Lisboa',
                'district_id': distr('Lisboa').id,
                'subcategory_id': subcat('Carros').id,
                'user_id': user('Carlos Carvalho').user_id,
            },
            {
                'title': 'Xiaomi Mi Home Security Camera Basic 1080p',
                'description':  'A Xiaomi Mi Home Security Camera Basic 1080p é uma camera de segurança doméstica com recursos avançados. Algumas de suas características incluem: resolução 1080p, visão noturna, detenção de movimento, áudio bidirecional, armazenamento em nuvem, conectividade Wi-Fi, panorâmica e inclinação, e configurações de privacidade. A camera oferece qualidade de vídeo nítida e clara; permite visualização noturna; deteta movimentos e envia notificações; possui áudio bidirecional; armazena vídeos na nuvem; permite acesso remoto via Wi-Fi; possui funcionalidade de panorâmica e inclinação; e oferece recursos de privacidade para proteger dados e privacidade.',
                'main_image_url': 'item_id5_img_main.jpg',
                'image1_url': 'item_id5_img1.jpg',
                'image2_url': 'item_id5_img2.jpg',
                'image3_url': '',
                'image4_url': '',
                'price': dec(30.00).quantize(dec('0.01')),
                'address_line': 'Rua do Sol',
                'zip_code': '',
                'district_id': distr('Porto').id,
                'subcategory_id': subcat('Outros Eletrónicos').id,
                'user_id': user('Diego Domingues').user_id,
            },
            {
                'title': 'Cadeiras de Escritório',
                'description':  'Vendo 3 cadeiras de Escritório eme bom estado, a 50€ cada uma.',
                'main_image_url': 'item_id6_img_main.jpg',
                'image1_url': '',
                'image2_url': '',
                'image3_url': '',
                'image4_url': '',
                'price': dec(150.00).quantize(dec('0.01')),
                'address_line': '',
                'zip_code': '1250-100 Lisboa',
                'district_id': distr('Lisboa').id,
                'subcategory_id': subcat('Outro Mobiliário').id,
                'user_id': user('Carlos Carvalho').user_id,
            },
            {
                'title': 'Apple Iphone X',
                'description':  'Smartphone Apple Iphone X',
                'main_image_url': 'item_id7_img_main.jpg',
                'image1_url': 'item_id7_img1.jpg',
                'image2_url': 'item_id7_img2.jpg',
                'image3_url': '',
                'image4_url': '',
                'price': dec(199.999).quantize(dec('0.01')),
                'address_line': '',
                'zip_code': '',
                'district_id': distr('Aveiro').id,
                'subcategory_id': subcat('Smartphones').id,
                'user_id': user('Augusto Andrade').user_id,
            },
            {
                'title': 'Livros',
                'description':  'Vendo 9 livros cada um a 5€ cada.',
                'main_image_url': 'item_id8_img_main.jpg',
                'image1_url': '',
                'image2_url': '',
                'image3_url': '',
                'image4_url': '',
                'price': dec(45.000).quantize(dec('0.01')),
                'address_line': 'Rua dos Moinhos',
                'zip_code': '4900-341 Viana do Castelo',
                'district_id': distr('Viana do Castelo').id,
                'subcategory_id': subcat('Livros em Língua Estrangeira').id,
                'user_id': user('Eva Esteves').user_id,
            },
            {
                'title': 'Kit de viagem',
                'description':  'Vendo 1 kit de viagem com uma máscara facial, um desinfetante, um sabonete, umas toalhitas para as mãos e a bolsa para guardar todo o que precisa.',
                'main_image_url': 'item_id9_img_main.jpg',
                'image1_url': '',
                'image2_url': '',
                'image3_url': '',
                'image4_url': '',
                'price': dec(15.000).quantize(dec('0.01')),
                'address_line': 'Rua dos Moinhos',
                'zip_code': '4900-341 Viana do Castelo',
                'district_id': distr('Viana do Castelo').id,
                'subcategory_id': subcat('Saúde & Beleza').id,
                'user_id': user('Eva Esteves').user_id,
            },
            {
                'title': 'Nikon DSLR Camera',
                'description':  'A câmara Nikon DSLR é uma poderosa ferramenta fotográfica que combina tecnologia avançada e qualidade de imagem superior. Com um sensor de alta resolução e capacidade de capturar detalhes incríveis, esta câmara oferece imagens nítidas e vibrantes. Além disso, possui um sistema de autofoco rápido e preciso, permitindo capturar momentos precisos com facilidade. Com modos de disparo versáteis, incluindo fotografia em sequência e intervalos de tempo, a câmara Nikon DSLR é ideal para fotógrafos profissionais e entusiastas apaixonados pela arte da fotografia.',
                'main_image_url': 'item_id10_img_main.jpg',
                'image1_url': '',
                'image2_url': '',
                'image3_url': '',
                'image4_url': '',
                'price': dec(800.000).quantize(dec('0.01')),
                'address_line': 'Rua Nova',
                'zip_code': '8000-020 Faro',
                'district_id': distr('Faro').id,
                'subcategory_id': subcat('Câmaras Fotográficas').id,
                'user_id': user('Fábio Fernandes').user_id,
            },
            {
                'title': 'Pintura',
                'description':  'Quadro expressivo e vibrante, uma obra única de arte contemporânea.',
                'main_image_url': 'item_id11_img_main.jpg',
                'image1_url': '',
                'image2_url': '',
                'image3_url': '',
                'image4_url': '',
                'price': dec(45.000).quantize(dec('0.01')),
                'address_line': 'Av. da Praia',
                'zip_code': '2520-038 Peniche',
                'district_id': distr('Leiria').id,
                'subcategory_id': subcat('Diversos').id,
                'user_id': user('Gabriela Gomes').user_id,
            },
            {
                'title': 'Livro',
                'description':  'Vendo livro em inglês.',
                'main_image_url': 'item_id12_img_main.jpg',
                'image1_url': '',
                'image2_url': '',
                'image3_url': '',
                'image4_url': '',
                'price': dec(5.000).quantize(dec('0.01')),
                'address_line': 'Rua da Carreira',
                'zip_code': '9000-036 Funchal',
                'district_id': distr('Ilha da Madeira').id,
                'subcategory_id': subcat('Livros em Língua Estrangeira').id,
                'user_id': user('José Faria').user_id,
            },
        ),
    )
    
    
def insert_msgs():
    insert_rows(
        label = 'MSG',
        summary = lambda msg: f"Created msg id: {msg.id}",
        insert_function = send_msg,
        rows = (
            {
                'user1_id': user('Eva Esteves').user_id,
                'user2_id': user('Carlos Carvalho').user_id,
                'item_id': item('BMW 5 Series Gran Turismo 535i RWD').id,
                'message': 'Boa tarde. O carro ainda está para venda?',
            },
            {
                'user1_id': user('Carlos Carvalho').user_id,
                'user2_id': user('Eva Esteves').user_id,
                'item_id': item('BMW 5 Series Gran Turismo 535i RWD').id,
                'message': 'Boa tarde. Sim, ainda está. Quer agendar para vê-lo?',
            },
            {
                'user1_id': user('Eva Esteves').user_id,
                'user2_id': user('Carlos Carvalho').user_id,
                'item_id': item('BMW 5 Series Gran Turismo 535i RWD').id,
                'message': 'Tenho disponibilidade para vê-lo no próximo fim de semana.',
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