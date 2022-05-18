from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_scheme import DailyText
from model import predict
import pandas as pd

DATABASE_URL = "postgresql+psycopg2://db_login@postgres/api_database"
engine = create_engine(DATABASE_URL, echo=True)
DBSession = sessionmaker(bind=engine)

with DBSession() as session:
  texts = session.query(DailyText).filter(DailyText.emotion == None)
  if texts:
    df = pd.read_sql_query(sql = texts.statement, con=engine)
    predictions = predict(df)
    for query, prediction in zip(texts.all(), predictions.to_numpy()):
      query.emotion = prediction
      session.add(query)

    try:
      session.commit()
    except:
      print("Failed to commit the prediction")