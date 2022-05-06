from database_scheme import Base
from sqlalchemy import create_engine
import os

# engine = create_engine(
#   "postgresql+psycopg2://api_accs:root@localhost/test_api",
#   echo=True, 
# )

engine = create_engine(os.environ.get("DATABASE_URL"), echo=True)

Base.metadata.create_all(engine)


# docker-compose up --build
# docker exec -it api_api_1 python app/database_create.py