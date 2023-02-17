from pydantic import BaseModel, Field
from uuid import UUID
from typing import Union, Optional


class Book(BaseModel):
    # id: Union[UUID, None] = None
    title: str = Field(minLength=4, max_length=15)
    description: Optional[str] = Field(max_length=100)
    rating: int = Field(gt=-1, lt=101)
