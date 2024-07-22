from typing import List, Optional

from pydantic import BaseModel


class WordDetails(BaseModel):
    word: str
    definitions: Optional[List[str]] = None
    synonyms: Optional[List[str]] = None
    translations: Optional[List[str]] = None
    examples: Optional[List[str]] = None


class WordOnly(BaseModel):
    word: str
