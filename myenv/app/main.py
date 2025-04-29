from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session
from .utils import convert_to_pydantic_list

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
@app.get("/", response_model=list[schemas.Post])
async def root(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return convert_to_pydantic_list(posts, schemas.Post)

@app.get("/posts", response_model=list[schemas.Post])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return convert_to_pydantic_list(posts, schemas.Post)


# 

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{post_id}", response_model=schemas.Post)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post:
        return post
    raise HTTPException(status_code=404, detail="Post not found")



@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post:
        db.delete(post)
        db.commit()
        return {"message": "Post deleted"}
    raise HTTPException(status_code=404, detail="Post not found")



@app.put("/posts/{post_id}", response_model=schemas.Post)
async def update_post(post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    existing_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if existing_post:
        existing_post.title = post.title
        existing_post.content = post.content
        existing_post.published = post.published
        db.commit()
        db.refresh(existing_post)
        return existing_post
    raise HTTPException(status_code=404, detail="Post not found")

