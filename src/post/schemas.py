from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    description: str | None = None


class PostCreate(PostBase):
    owner_id: int

    class Config:
        orm_mode = True


class PostRead(BaseModel):
    id: int
    title: str
    description: str
    owner_id: int

    class Config:
        orm_mode = True


class LikeBase(BaseModel):
    like: bool
    post_id: int
    owner_id: int| None = None
