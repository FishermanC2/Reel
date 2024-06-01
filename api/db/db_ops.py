from datetime import datetime, timedelta
import time
from ..extensions import db
from ..hook.models import Hook
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

DEFAULT_DB_FLUSH_THRESHOLD = datetime.utcnow() - timedelta(minutes=5)

def run_periodic_db_refresh(interval):
    engine = create_engine('sqlite:///D:\\Reel\\api\\db\\hooks.db', echo=True)
    session_factory = sessionmaker(bind=engine)
    db_session = scoped_session(session_factory)
    while True:
        DBOperations.refresh_db(db_session)
        time.sleep(interval)

class DBOperations:
    @classmethod
    def refresh_db(cls, session):
        old_hooks = session.query(Hook).filter(Hook.last_update < DEFAULT_DB_FLUSH_THRESHOLD).all()
        for hook in old_hooks:
            session.delete(hook)
        
        session.commit()
