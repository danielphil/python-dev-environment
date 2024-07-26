from fastapi import Depends, FastAPI, HTTPException
from pytest import Session

from python_dev_environment import database, models, schemas


app = FastAPI()
database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def get_root():
    return "Hello world!"


@app.get("/user/{user_id}")
def get_user(user_id: int, db_session: Session = Depends(get_db)) -> schemas.User:
    user = db_session.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User ID {user_id} not found")
    return user


@app.put("/user")
def create_user(
    details: schemas.UserDetails, db_session: Session = Depends(get_db)
) -> schemas.User:
    new_user = models.User(name=details.name)
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)
    return new_user
