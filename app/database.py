from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# format of a connection string that we have to pass into sqlalchamy.
# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip_address/hostname>/<database_name>' 

# SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:1234@LocalHost/fastapi'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# create an engine object

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# the below code is used to connect to the database using psycopg2

# import psycopg2
# from psycopg2.extras import RealDictCursor

# while True:  # the below code will keep trying to connect to the database until it is connected

#     try:
#         conn = psycopg2.connect(host='localhost', dbname='fastapi', user='postgres', password='1234', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connected successfully')
#         break
#     except Exception as error:
#         print('Database connection failed')
#         print(f'Error: {error}')
#         time.sleep(5)

# my_posts = [{'title' : 'title of post 1', 
#              'content' : 'content of post 1',
#              'id' : 1},
#              {'title' : 'favorite foods', 
#              'content' : 'I like pizza',
#              'id' : 2}]

# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p
        
# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i 