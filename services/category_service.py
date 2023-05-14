from typing import List
from data.models import Category

def list_category(count: int) -> List[Category]:
    return [
        Category(
            id = 1,
            category_name = 'Veículos',
            icon = 'car.svg',
            weblink = 'category.html',
            count_items_category = 35,
        ),
        Category(
            id = 2,
            category_name = 'Eletrónicos',
            icon = 'laptop.svg',
            weblink = 'category.html',
            count_items_category = 22,
        ),
        Category(
            id = 3,
            category_name = 'Mobiliário',
            icon = 'furniture.svg',
            weblink = 'category.html',
            count_items_category = 21,
        ),
        Category(
            id = 4,
            category_name = 'Vestuário',
            icon = 'tshirt.svg',
            weblink = 'category.html',
            count_items_category = 25,
        ),
        Category(
            id = 5,
            category_name = 'Acessórios',
            icon = 'watch.svg',
            weblink = 'category.html',
            count_items_category = 15,
        ),
        Category(
            id = 6,
            category_name = 'Saúde & Beleza',
            icon = 'hospital.svg',
            weblink = 'category.html',
            count_items_category = 22,
        ),
        Category(
            id = 7,
            category_name = 'Livros',
            icon = 'education.svg',
            weblink = 'category.html',
            count_items_category = 42,
        ),
        Category(
            id = 8,
            category_name = 'Jogos',
            icon = 'controller.svg',
            weblink = 'category.html',
            count_items_category = 32,
        ),
        Category(
            id = 9,
            category_name = 'Habitação',
            icon = 'real-estate.svg',
            weblink = 'category.html',
            count_items_category = 65,
        ),
        Category(
            id = 10,
            category_name = 'Empregos',
            icon = 'jobs.svg',
            weblink = 'category.html',
            count_items_category = 44,
        ),
        Category(
            id = 11,
            category_name = 'Outros',
            icon = 'matrimony.svg',
            weblink = 'category.html',
            count_items_category = 55,
        ),
    ][:count]