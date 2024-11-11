from fastapi import FastAPI, Depends, status, HTTPException, Response
from . import  models, schemas
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
# from  .routers import blog, user, authentication

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=201)
def create(request:schemas.Blog, db:Session= Depends(get_db)):
    new_blog=models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog')
def all(db:Session= Depends(get_db)):
    blogs=db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code=200, response_model=schemas.ShowBlog)
def show(id, db:Session= Depends(get_db)):

    blog=db.query(models.Blog).filter(models.Blog.id==id).first()

    if not blog:
        raise HTTPException(status_code=404, detail="id not found")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"detail":"blog with the id not found"}
    return blog


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db:Session= Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="id do not exist")

    else:
        blog.delete(synchronize_session=False)
    db.commit()
    return "done"

@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db:Session= Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="id do not exist")

    else:
        blog.update(request)
    db.commit()
    return "done"

    
