import sqlalchemy
# import pyodbc
# import urllib
from fastapi import FastAPI, HTTPException
import uvicorn
import os
# import psycopg2
# from database import metadata, users
from database_scheme import User, DailyText
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from datetime import date, datetime


engine = sqlalchemy.create_engine(os.environ.get("DATABASE_URL"), echo=True)
DBSession = sessionmaker(bind=engine)

app = FastAPI()

@app.get("/seed")
async def add_usr():
  with DBSession() as session:
    jean = User(username="jean", first_name="zobe", last_name="mbb")
    session.add(jean)

    oui = DailyText(text="oui", user=jean)
    session.add(oui)
    try:
      session.commit()
      return 200
    except:
      raise HTTPException(status_code=500, detail="Can't seed")

# User methods

class UserInfo(BaseModel):
  username: str
  last_name: str
  first_name: str
  is_admin: bool = False
  # password: str

@app.post("/user")
async def register(user_info: UserInfo):
  new_user = User(
    username = user_info.username,
    first_name = user_info.first_name,
    last_name = user_info.last_name,
    is_admin = user_info.is_admin
  )

  with DBSession() as session:
    session.add(new_user)
    try:
      session.commit()
      return 200
    except:
      raise HTTPException(status_code=500, detail="Can't add this user, check types and unique username")

@app.put("/user")
async def modify_user(user_info: UserInfo):
  with DBSession() as session:
    user = session.query(User).filter(User.username == user_info.username).first()
    if user:
      user.first_name = user_info.first_name
      user.last_name = user_info.last_name
      user.is_admin = user_info.is_admin
    else:
      raise HTTPException(status_code=404, detail="Can't find this user")

    try:
      session.add(user)
      session.commit()
      return 200
    except:
      raise HTTPException(status_code=500, detail="Can't commit changes")

@app.delete("/user")
async def delete_user(username: str):
  with DBSession() as session:
    user = session.query(User).filter(User.username == username).first()
    if user:
      try:
        session.delete(user)
        session.commit()
        return 200
      except:
        raise HTTPException(status_code=500, detail="Can't delete this user")
    else:
      raise HTTPException(status_code=404, detail="Can't find any user with this username")

@app.get("/user")
async def get_user_info(username: str):
  # return all the infos for a given user
  with DBSession() as session:
    user = session.query(User).filter(User.username == username).first()
    if user:
      return user
    else:
      raise HTTPException(status_code=404, detail="Can't find any user with this username")

@app.get("/userlist")
async def get_users_list(admins: bool = True):
  # Gets all the users
  with DBSession() as session:
    users = session.query(User)
    if not admins: users = users.filter(User.is_admin == False)
    users = users.all()

    if users:
      return users
    else:
      raise HTTPException(status_code=404, detail="No user corresponding to the filter")

# Text methods

class Text(BaseModel):
  text: str
  user_username: str

@app.post("/text")
async def post_text(text: Text):
  with DBSession() as session:
    # if there already is an entry today, update it. Else, create a new one
    entry = session.query(DailyText).filter(DailyText.user_username==text.user_username, DailyText.date == date.today()).first()
    if entry:
      entry.text = text.text
    else:
      entry = DailyText(
        text = text.text,
        user_username = text.user_username
      )
    session.add(entry)

    try:
      session.commit()
      return 200
    except:
      raise HTTPException(status_code=500, detail="Can't commit the text")

@app.get("/text")
async def get_text(username: str, date: str):
  # get a text for a given user at a given date. Return an empty string if there isn't anything 
  date_object = datetime.strptime(date, "%Y-%m-%d").date()
  with DBSession() as session:
    text = session.query(DailyText).filter(DailyText.user_username==username, DailyText.date == date_object).first()       
  if text:
    return text
  else:
    return {"text": f"No entry on the {date}"}

@app.get("/emotions")
def get_emotions(start_date: str, end_date: str | None = None, username: str | None = None):
  with DBSession() as session:
    q = session.query(DailyText)

    if username: q = q.filter(DailyText.user_username==username)
    if end_date:
      q = q.filter(DailyText.date >= start_date, DailyText.date <= end_date)
    else:
      q = q.filter(DailyText.date == start_date)

    q = q.all()
    # This will change in order to return emotions percentages when the model will be done
    if q:
      return q
    else:
      raise HTTPException(status_code=404, detail="No text corresponding to the filter") 

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))