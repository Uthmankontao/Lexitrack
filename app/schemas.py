from pydantic import BaseModel, Field, EmailStr, conint
from datetime import datetime
from typing import Optional, List



# USER SCHEMAS

class UserBase(BaseModel):
    email: EmailStr
    password: str

class CreateUser(UserBase):
    pass 

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None



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