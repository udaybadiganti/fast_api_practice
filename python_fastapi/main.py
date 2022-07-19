from typing import Optional

from fastapi import FastAPI
from enum import Enum

from pydantic import BaseModel


class Student(str, Enum):
    uday = 'uday'
    vinod = 'vinod'
    nani = 'nani'


app = FastAPI()


@app.get('/')
async def home():
    return {'name': 'uday', 'city': 'vizianagaram', }


@app.get('/item/{item_id}')
async def item(item_id:int):
    return {'item_id': item_id}


@app.get('/model/{model_name}')
async def get_model(model_name: Student):
    if model_name == Student.nani:
        return {'model_name': model_name, 'message': 'this is machine learning model'}
    if model_name.value == 'uday':
        return {'model_name': model_name, 'message': 'this is deep learning model'}
    return {'model_name': model_name, 'message': 'Have some residuals'}


@app.get("/blog")
async def blog(limit=10, published: bool = True, sort: Optional[str] = None):
    if published:
        return {"file_path": f"{limit} published blogs from db"}
    else:
        return {"file_path": f"{limit} blogs from db"}


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.post('/create_blog')
async def create_blog(request: Blog):
    return {'data': f'Blog is created title as {request.title}'}