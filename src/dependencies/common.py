from typing import Annotated, Optional

from fastapi import Depends

from src.core.constants import CITIES_NUMBER
from src.enums.sql import OrderEnum


async def query_params_get_list(
    offset: int = 0,
    limit: int = CITIES_NUMBER,
    sort_by: Optional[str] = None,
    sort: Optional[str] = OrderEnum.ASCENDING.value
) -> dict:
    """
    Common query parameters to get a list of objects.

    Args:
        - `offset`: number of skip;
        - `limit`: limit the number of results;
        - `sort_by`: sort by field name;
        - `sort`: ascending or descending.
    """
    return {
        'offset': offset,
        'limit': limit,
        'order': sort,
        'order_by_field': sort_by
    }


QueryParamDeps: type[dict] = Annotated[dict, Depends(query_params_get_list)]
