from typing import List, Optional
from fastapi import APIRouter, Depends,HTTPException
from googletrans import Translator
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, DESCENDING

from db import get_db
from shemas.request import SortingOrder
from shemas.response import WordDetails, WordOnly

router = APIRouter()
translator = Translator()


@router.get("/word/{word}", response_model=WordDetails)
async def get_word_details(word: str,
                           db: AsyncIOMotorClient = Depends(get_db)
                           ):
    word_data = await db.words.find_one({"word": word})
    if word_data:
        return word_data

    translation = translator.translate(word, dest='en')
    if not translation:
        raise HTTPException(status_code=404, detail="Word not found")
    # todo free solutions don't provide additional info
    word_details = {
        "word": word,
        "definitions": ["Example definition"],
        "synonyms": ["Example synonym"],
        "translations": [translation.text],
        "examples": ["Example sentence"]
    }
    await db.words.insert_one(word_details)
    return word_details


@router.get("/words/", response_model=List[WordDetails | WordOnly])
async def list_words(
    skip: int = 0,
    limit: int = 10,
    word: Optional[str] = None,
    sort: Optional[SortingOrder] = SortingOrder.ASC,
    include_details: Optional[bool] = False,
    db: AsyncIOMotorClient = Depends(get_db)
):
    query = {}
    if word:
        query["word"] = {"$regex": word, "$options": "i"}

    sort_order = ASCENDING if sort == SortingOrder.ASC else DESCENDING
    cursor = db.words.find(query).skip(skip).limit(limit).sort("word", sort_order)
    if include_details:
        return [WordDetails(**word) async for word in cursor]
    else:
        return [WordOnly(**word) async for word in cursor]


@router.delete("/word/{word}", response_model=dict)
async def delete_word(word: str,
                      db: AsyncIOMotorClient = Depends(get_db)
                      ):
    result = await db.words.delete_one({"word": word})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Word not found")
    return {"message": "Word deleted"}
