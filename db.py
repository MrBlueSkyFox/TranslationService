import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import logging

from settings import config

load_dotenv()

db_client: AsyncIOMotorClient = None


async def get_db() -> AsyncIOMotorClient:
    db_name = config.DB_NAME
    return db_client[db_name]


async def connect_and_init_db():
    global db_client
    try:
        db_client = AsyncIOMotorClient(
            config.db_url,
            # username=config.DB_USER,
            # password=config.DB_PASS,
            maxPoolSize=config.DB_POOL_SIZE_MAX,
            minPoolSize=config.DB_POOL_SIZE_MIN,
            uuidRepresentation="standard",
        )
        logging.info('Connected to mongo.')
        print(config.db_url)
    except Exception as e:
        logging.exception(f'Could not connect to mongo: {e}')
        raise


async def close_db_connect():
    global db_client
    if db_client is None:
        logging.warning('Connection is None, nothing to close.')
        return
    db_client.close()
    db_client = None
    logging.info('Mongo connection closed.')
