from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import time
from ..hook.models import Hook

# After this threshold, an hook is considered 'old' and is removed
DEFAULT_DB_FLUSH_THRESHOLD = datetime.utcnow() - timedelta(minutes=5)

def run_periodic_db_refresh(app, interval):
    """
    Create a scoped session to connect to the db (required for threads)
    """
    engine = create_engine('sqlite:///D:\\Reel\\api\\db\\hooks.db', echo=True)
    session_factory = sessionmaker(bind=engine)
    db_session = scoped_session(session_factory)
    while True:
        old_hooks_count = DBOperations.refresh_db(db_session)
        app.logger.info(f"Refreshed DB, deleted {old_hooks_count} old hooks. ")
        time.sleep(interval)

class DBOperations:
    @classmethod
    def refresh_db(cls, session):
        """
        Remove old hooks from db
        """
        old_hooks = session.query(Hook).filter(Hook.last_update < DEFAULT_DB_FLUSH_THRESHOLD).all()
        for hook in old_hooks:
            session.delete(hook)
        
        session.commit()
        return len(old_hooks)
