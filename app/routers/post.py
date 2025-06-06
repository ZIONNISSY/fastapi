from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session 
from sqlalchemy import func
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix= "/posts", tags=["Posts"])

@router.get("/", response_model= List[schemas.PostOut]) # to get all the posts
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), Limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() # to fetch the posts which are created by the current user
    
    print(Limit, skip)

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all() # tp fetch all the posts from the database

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()
            # this above query is to fetch the total number of votes with the posts details          

    return posts

@router.post("/", status_code= status.HTTP_201_CREATED, response_model=schemas.PostResponse) # to create a new post
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit() # to save the chages

    # print(current_user) # it prints the current_user object which is the user who is logged in
    print(current_user.email) # it prints the email of the current user

    # (title=post.title, content=post.content, published=post.published) instead of doing this we can use { **post,dict() } to pass the values
    new_post = models.Post(owner_id=current_user.id, **post.dict()) # it createas a new post object with the values from the post object
                        #  owner_id = current_user.id to add the owner_id to the post 
    db.add(new_post) # to add the new post to our database
    db.commit() # to save the changes
    db.refresh(new_post) # to fetch the new post from the database

    return new_post

@router.get("/{id}", response_model=schemas.PostOut)  # to get a post by id
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()

    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f'Post with id: {id} not found')
    
    return post

@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)  # to delete a post by id
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)  # query to get the post with the id
    post = post_query.first() # to get the first post with the id

    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f'Post with id: {id} does not exit')
    
    if post.owner_id != current_user.id: # to check if the post belongs to the current user
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail = f'Not authorized to perform requested action')
    
    post.delete(synchronize_session=False) # runing the query to delete the post
    db.commit()
    
    return Response(status_code= status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.PostResponse)  # to update a post by id
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f'Post with id: {id} does not exit')
    
    if post.owner_id != current_user.id: # to check if the post belongs to the current user
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail= f'Not authorized to perform requested action')
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return post_query.first()