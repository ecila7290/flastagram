import config

from flask import Flask
from flask_cors import CORS
from sqlalchemy import create_engine

from service import UserService, PostService
from model import UserDao, PostDao
from view import create_endpoints

class Service:
    pass

def create_app(test_config=None):
    app=Flask(__name__)
    CORS(app)

    if test_config is None:
        app.config.from_pyfile('config.py')
    else:
        app.config.update(test_config)

    database=create_engine(app.config['DB_URL'], encoding='utf-8', max_overflow=0)

    # persistence layer
    user_dao=UserDao(database)
    post_dao=PostDao(database)

    # business layer
    services=Service()
    services.user_service=UserService(user_dao,app.config)
    services.post_service=PostService(post_dao,app.config)
    
    # create endpoint
    create_endpoints(app, services)

    return app