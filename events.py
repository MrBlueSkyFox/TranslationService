from typing import Callable, Awaitable

from fastapi import FastAPI

from db import connect_and_init_db


def startup(app: FastAPI) -> Callable[[], Awaitable[None]]:
    async def _startup() -> None:
        await connect_and_init_db()

        return None

    return _startup
