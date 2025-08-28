from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class SummaryContent(BaseModel):
    short: str = Field(default="")
    detailed: str = Field(default="")

class QAItem(BaseModel):
    question: str
    answer: str = ""

class SummaryBase(BaseModel):
    source_type: str
    title: str
    summary: SummaryContent
    questions: List[QAItem]

class SummaryCreate(SummaryBase):
    created_at: datetime
    updated_at: datetime

class SummaryRead(SummaryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class URL(BaseModel):
    url : str