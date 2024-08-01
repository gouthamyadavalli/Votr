import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import Topics
import config
from votr import celery

def connect():
    """Connects to database and returns a session"""
    uri = config.SQLALCHEMY_DATABASE_URI
    con = sqlalchemy.create_engine(uri)

    Session = sessionmaker(bind=con)

    session = Session()

    return con, session

@celery.task
def close_poll(topic_id):
    topic = session.query(Topics).get(topic_id)
    topic.status = False
    session.commit()