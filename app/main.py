import sqlalchemy
# import pyodbc
# import urllib
from fastapi import FastAPI
import uvicorn
import os
# import psycopg2
# from database import metadata, users
from database_scheme import User, Base
from sqlalchemy.orm import sessionmaker

# pwd = "Xpwc4XJkys6zpaD"
# params = urllib.parse.quote_plus(
#   r"driver={ODBC Driver 18 for SQL Server};" +
#   r"Server=tcp:zen.database.windows.net,1433;" + 
#   r"Database=ZEN;" +
#   r"Uid=zen_root;"
#   f"Pwd={pwd};"
#   r"Encrypt=yes;"
#   r"TrustServerCertificate=no;"
#   r"Connection Timeout=30;"
# )

# params = urllib.parse.quote_plus(
#   f"zen_root:{pwd}@zen.database.windows.net:1433/ZEN?trusted_connection=yes&driver=obdc+driver+18+for+sql+server" # 
# )

# print(params)

# # connection_string = f"mssql+pyodbc:///?obdc_connect={params}"
# connection_string = f"mssql+pyodbc://{params}"


# print(connection_string)

# azure_engine = sqlalchemy.create_engine(connection_string, echo=True)
# azure_engine = azure_engine.connect()

# print("ok")
engine = sqlalchemy.create_engine(os.environ.get("DATABASE_URL"), echo=True)
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = FastAPI()

@app.get('/')
async def home():
  return "Hello world !"

@app.get("/add")
async def add_usr():
  try:
    jean = User(username="jean", first_name="zobe", last_name="mbb")
    session.add(jean)
    session.commit()
    return 200
  except:
    return 100

@app.get("/list")
async def list():
  # users = User.query.all()
  users = session.query(User).all()
  return users

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

# engine = sqlalchemy.create_engine(
#   "postgresql+psycopg2://api_accs:root@localhost/test_api",
#   echo=True, 
# )
# metadata.create_all(engine)
# conn = engine.connect()

# Base.metadata.create_all(engine)



# jean = User(username="jean", first_name="zobe", last_name="mbb")
# session.add(jean)
# session.commit()
# print(engine)


print("Hello World!")

# engine = sqlalchemy.create_engine(os.environ.get("DATABASE_URL"), echo=True)

