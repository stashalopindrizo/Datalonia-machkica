from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class RememberIn(BaseModel):
    text: str = Field(..., min_length=1)
    tags: List[str] = []

class MemoryItem(BaseModel):
    id: str
    text: str
    tags: List[str]
    created_at: datetime

class SearchIn(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int = 5

class SearchOutItem(BaseModel):
    item: MemoryItem
    score: float

class BrainStats(BaseModel):
    total: int
    tags: List[str]