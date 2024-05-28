from api.extensions import db

class Command(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hook_id = db.Column(db.Integer, nullable=False)
    command = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f'<Command {self.command}>'
    