from typing import List
from decimal import Decimal as dec
from data.models import District, Region


def location_district(count: int) -> List[District]:
    return [
        District(
            id = 2,
            district_name = 'Viana do Castelo',
            
        ),
        District(
            id = 3,
            district_name = 'Braga',
            
        ),
        District(
            id = 4,
            district_name = 'Vila Real',
            
        ),
        District(
            id = 5,
            district_name = 'Bragança',
            
        ),
        District(
            id = 6,
            district_name = 'Porto',
            
        ),
        District(
            id = 7,
            district_name = 'Aveiro',
            
        ),
        District(
            id = 8,
            district_name = 'Viseu',
            
        ),
        District(
            id = 9,
            district_name = 'Guarda',
            
        ),
        District(
            id = 10,
            district_name = 'Coimbra',
            
        ),
        District(
            id = 11,
            district_name = 'Castelo Branco',
            
        ),
        District(
            id = 12,
            district_name = 'Leiria',
            
        ),
        District(
            id = 13,
            district_name = 'Santarém',
            
        ),
        District(
            id = 14,
            district_name = 'Portalegre',
            
        ),
        District(
            id = 15,
            district_name = 'Lisboa',
            
        ),
        District(
            id = 16,
            district_name = 'Santarém',
            
        ),
        District(
            id = 17,
            district_name = 'Évora',
            
        ),
        District(
            id = 18,
            district_name = 'Setúbal',
            
        ),
        District(
            id = 19,
            district_name = 'Beja',
            
        ),
        District(
            id = 20,
            district_name = 'Faro',
            
        ),
        District(
            id = 21,
            district_name = 'Madeira',
            
        ),
        District(
            id = 22,
            district_name = 'Açores',
            
        ),
    ][:count]     
        
        






def location_region(count: int) -> List[Region]:
    return [
        Region(
            id = 1,
            region_name = 'Oeiras',
            district_name = 'Lisboa',
        ),
    ][:count]   
            