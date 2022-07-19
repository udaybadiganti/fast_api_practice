from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schema, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED)
async def create(request: schema.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, body = request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.put('/update/{ids}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schema.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    print(blog)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{id} not available')
    blog.update(request.dict())
    db.commit()
    return {'updated'}


@app.get('/show', response_model=List[schema.ShowBlog])
async def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} is not available.")
    return blogs


@app.get('/show/{id}', status_code=200, response_model=schema.ShowBlog)
async def show(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} is not available.")
    return blog


@app.delete('/destroy/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def destroy(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} is not available.")
    blog.delete(synchronize_session=False)
    db.commit()
    return {'deleted'}


@app.post('/user', status_code=status.HTTP_201_CREATED)
def create_user(request: schema.User, db: Session = Depends(get_db)):
    new_user = models.User(**request.dict())
    db.add(new_user)
    db.commit()
    db.refresh()

    return new_user