from typing import List
from data.models import Subcategory


def list_subcategory(count: int) -> List[Subcategory]:
    return [
        Subcategory(
            id = 1,
            subcategory_name = 'Carros',
            category_name = 'Veículos',
            count_items_subcategory = 10,
        ),
        Subcategory(
            id = 2,
            subcategory_name = 'Motociclos',
            category_name = 'Veículos',
            count_items_subcategory = 10,
        ),
        Subcategory(
            id = 3,
            subcategory_name = 'Veículos Elétricos',
            category_name = 'Veículos',
            count_items_subcategory = 15,
        ),
        Subcategory(
            id = 4,
            subcategory_name = 'Eletrónicos',
            category_name = 'Computadores Desktop',
            count_items_subcategory = 7,
        ),
        Subcategory(
            id = 5,
            subcategory_name = 'Eletrónicos',
            category_name = 'Portáteis',
            count_items_subcategory = 5,
        ),
        Subcategory(
            id = 6,
            subcategory_name = 'Eletrónicos',
            category_name = 'Tablets',
            count_items_subcategory = 3,
        ),
    ][:count]