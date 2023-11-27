import asyncio
import csv
from pathlib import Path

from tqdm import tqdm

from src.api.v1.schemas.request.city import CityCreateSchema
from src.core.constants import CITY_DATA_FILE
from src.dependencies.unit_of_work import get_uow
from src.services.city import CityService


async def load_cities_data(
    uow,
    file_path: Path | str = CITY_DATA_FILE
) -> None:
    with open(file_path, encoding='utf-8') as file:
        for row in tqdm(list(csv.DictReader(file))):
            city_schema = CityCreateSchema(
                name=row.get('city'),
                country=row.get('country'),
                latitude=row.get('latitude'),
                longitude=row.get('longitude')
            )
            await CityService.create(uow, city_schema.model_dump())


async def main() -> None:
    uow = next(get_uow())
    await load_cities_data(uow)


if __name__ == '__main__':
    asyncio.run(main())
