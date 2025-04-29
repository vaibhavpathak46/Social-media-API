from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    title: str
    content: str
    published: bool = True

    class Config:
        from_attributes = True