from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    # co jesli nie istnieje taki post na któreogo głosujemy:
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {vote.post_id} doesnt exist")
    #sprawdzamy czy głos istnieje juz
    # dodajemy w nawiasie dwa warunki, bo jedna osoba mogla polubic wiele postow)
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                              models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1: #Jesli user chce polubić post:
        if found_vote: # jesli istnieje
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User {current_user.id} like this post {vote.post_id} already")
        #tu jesli nie istnieje dodajemy vote:
        new_vote = models.Vote(post_id = vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "succesly added a vote"}

    else: #jesli user chce usunąc vote
        if not found_vote: #jesli taki vote nie istnieje
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"vote doesnt exist")
        # jesli istnieje
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "succesfully deleted vote"}
