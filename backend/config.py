import os

class Config:

    SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL','postgresql://postgres:qwer4321@localhost:5432/task_manager_db')


    SQLALCHEMY_TRACK_MODIFICATIONS= False

    JWT_SECRET_KEY= os.getenv('JWT_SECRET_KEY', 'a3f5e7c2b9d1e8f4a0c3d6e7b8a9f0c1e2d3f4a5b6c7d8e9f0a1b2c3d4e5f6a7')

    DEBUG= True