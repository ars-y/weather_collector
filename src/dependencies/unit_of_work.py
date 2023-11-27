from typing import Any, Annotated, Generator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.sessions import LocalSession
from src.units.unit_of_work import UnitOfWork


def get_uow() -> Generator[AsyncSession, Any, Any]:
    """Generates Unit Of Work."""
    yield UnitOfWork(LocalSession)


UOWDep: type[UnitOfWork] = Annotated[UnitOfWork, Depends(get_uow)]
