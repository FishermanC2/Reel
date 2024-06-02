from api.extensions import db

class Command(db.Model):
    """
    Represents a command associated with a hook (sql alchemy model)
    """
    id = db.Column(db.Integer, primary_key=True)
    hook_id = db.Column(db.Integer, nullable=False)
    command = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        """Returns a string representation of the Command object."""
        return f'<Command {self.command}>'
