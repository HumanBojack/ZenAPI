import sqlalchemy
# import pyodbc
# import urllib
from fastapi import FastAPI
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

@app.get('/')
async def home():
  return "Bon Toutou"

@app.get("/add")
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
      return 500

class AddUser(BaseModel):
  username: str
  last_name: str
  first_name: str
  is_admin: bool = False
  # password: str

@app.post("/user")
async def register(user_info: AddUser):
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
      return 500

@app.get("/userlist")
async def get_users_list():
  #return the whole list of users
  pass

@app.get("/user")
async def get_user_info(username: str):
  # return all the infos for one user
  pass

@app.get("/text")
async def get_text(username: str, date: str):
  # get a text by user and date. Return an empty string if there isn't anything 
  date_object = datetime.strptime(date, "%Y-%m-%d").date()
  with DBSession() as session:
    text = session.query(DailyText).filter(DailyText.user_username==username, DailyText.date == date_object).first()       
  if text:
    return text
  else:
    return {"text": f"No entry on the {date}"}
  

class Text(BaseModel):
  text: str
  user_username: str

@app.post("/text")
async def post_text(text: Text):
  with DBSession() as session:
    # if there already is an entry today
    entry = session.query(DailyText).filter(DailyText.user_username==text.user_username, DailyText.date == date.today()).first()
    if entry:
      # update the current one
      entry.text = text.text
    else:
      # create a new entry
      entry = DailyText(
        text = text.text,
        user_username = text.user_username
      )
    session.add(entry)

    try:
      session.commit()
      return 200
    except:
      return 500


@app.get("/list")
async def list():
  with DBSession() as session:
    users = session.query(User).all()
    texts = session.query(DailyText).all()

  return [users, texts]

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))