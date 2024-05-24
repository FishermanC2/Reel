import logging
from models import db, Hook

class HookDB:
    def __init__(self):
        pass

    def register_hook(self) -> int:
        new_hook = Hook()
        db.session.add(new_hook)
        db.session.commit()
        logging.info(f"Hook {new_hook.id} created.")
        return new_hook.id
