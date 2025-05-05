from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from typing import Optional, List
from pydantic.types import conint

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)   # to tell the pydantic model to read the data even if it is not a dict

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    model_config = ConfigDict(from_attributes=True)   # to tell the pydantic model to read the data even if it is not a dict

class PostOut(BaseModel):
    Post: PostResponse
    votes: int 
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)   # to limit the value of dir to 1 or 0, if it is greater than 1 it will raise a validation error
    # if dir = 1 then it means upvote, if dir = 0 then it means downvote