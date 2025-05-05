from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import database, models, schemas, oauth2

router = APIRouter(prefix="/vote", tags=["Votes"])

@router.post("/", status_code= status.HTTP_201_CREATED) 
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'The post with the id {vote.post_id} does not exist')
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail= f'The user {current_user.id} has already voted on post {vote.post_id}')
        new_vote = models.Vote(user_id = current_user.id, post_id = vote.post_id)
        db.add(new_vote)
        db.commit()

        return {'message': 'Successfully added the vote'}
    else:
        if not found_vote:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'The post {vote.post_id} does not exist')
        vote_query.delete(synchronize_session = False)
        db.commit()

        return {'message': 'Successfully deleted the vote'}