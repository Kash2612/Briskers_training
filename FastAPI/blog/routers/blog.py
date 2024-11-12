from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, models, database, oauth2

from ..repository import blog

router= APIRouter(
    prefix="/blog",
    tags=["blogs"]
)
get_db=database.get_db

@router.get('/',response_model=List[schemas.ShowBlog])
def all(db:Session= Depends(database.get_db), current_user=Depends(oauth2.get_current_user)):
    # blogs=db.query(models.Blog).all()
    # return blogs

    return blog.get_all(db)

@router.post('/', status_code=201)
def create(request:schemas.Blog, db:Session= Depends(database.get_db),current_user=Depends(oauth2.get_current_user)):
    # new_blog=models.Blog(title=request.title, body=request.body, user_id=request.user_id)
    # db.add(new_blog)
    # db.commit()
    # db.refresh(new_blog)
    # return new_blog

    return blog.create(request, db)


@router.get('/{id}', status_code=200, response_model=schemas.ShowBlog)
def show(id, db:Session= Depends(get_db),current_user=Depends(oauth2.get_current_user)):

    # blog=db.query(models.Blog).filter(models.Blog.id==id).first()

    # if not blog:
    #     raise HTTPException(status_code=404, detail="id not found")
    #     # response.status_code=status.HTTP_404_NOT_FOUND
    #     # return {"detail":"blog with the id not found"}
    # return blog
    return blog.show(id, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db:Session= Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    # blog=db.query(models.Blog).filter(models.Blog.id==id)
    # if not blog.first():
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="id do not exist")

    # else:
    #     blog.delete(synchronize_session=False)
    # db.commit()
    # return "done"

    return blog.delete(id, db)

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db:Session= Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    # blog=db.query(models.Blog).filter(models.Blog.id==id)
    # if not blog.first():
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="id do not exist")

    # else:
    #     blog.update(request)
    # db.commit()
    # return "done"

    return blog.update(id,request, db)
