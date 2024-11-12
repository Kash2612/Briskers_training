from fastapi import FastAPI, Depends, status, HTTPException, Response
# from typing import List
from . import  models, schemas
from .database import engine, SessionLocal, get_db
# from sqlalchemy.orm import Session
# from .hashing import Hash
# from passlib.context import CryptContext
from  .routers import blog, user, authentication

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# @app.post('/blog', status_code=201, tags=["blogs"])
# def create(request:schemas.Blog, db:Session= Depends(get_db)):
#     new_blog=models.Blog(title=request.title, body=request.body, user_id=request.user_id)
#     db.add(new_blog)
#     db.commit()
#     db.refresh(new_blog)
#     return new_blog


# @app.get('/blog',response_model=List[schemas.ShowBlog], tags=["blogs"])
# def all(db:Session= Depends(get_db)):
#     blogs=db.query(models.Blog).all()
#     return blogs

# @app.get('/blog/{id}', status_code=200, response_model=schemas.ShowBlog, tags=["blogs"])
# def show(id, db:Session= Depends(get_db)):

#     blog=db.query(models.Blog).filter(models.Blog.id==id).first()

#     if not blog:
#         raise HTTPException(status_code=404, detail="id not found")
#         # response.status_code=status.HTTP_404_NOT_FOUND
#         # return {"detail":"blog with the id not found"}
#     return blog


# @app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["blogs"])
# def destroy(id, db:Session= Depends(get_db)):
#     blog=db.query(models.Blog).filter(models.Blog.id==id)
#     if not blog.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="id do not exist")

#     else:
#         blog.delete(synchronize_session=False)
#     db.commit()
#     return "done"

# @app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["blogs"])
# def update(id, request: schemas.Blog, db:Session= Depends(get_db)):
#     blog=db.query(models.Blog).filter(models.Blog.id==id)
#     if not blog.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="id do not exist")

#     else:
#         blog.update(request)
#     db.commit()
#     return "done"

    

# pwd_cxt=CryptContext(schemes=["bcrypt"],deprecated="auto")

# @app.post('/user', tags=["users"])
# def create_user( request:schemas.User, db:Session= Depends(get_db)):
#     # hashedPassword=pwd_cxt.hash(request.password)
#     # new_user=models.User(name=request.name, email=request.email, password=hashedPassword)
#     new_user=models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))

#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return new_user


# @app.get('/user/{id}', response_model=schemas.ShowUserBlogs, tags=["users"])
# def get_user(id:int, db:Session= Depends(get_db)):
#     user=db.query(models.User).filter(models.User.id==id).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} not found")
#     return user
