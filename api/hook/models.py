from datetime import datetime
from api.extensions import db

class Hook(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    last_update = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_agent = db.Column(db.String(255))
    ip_address = db.Column(db.String(45))  # 45 to accommodate IPv6 addresses
    screen_resolution = db.Column(db.String(50))
    timezone = db.Column(db.String(50))
    language = db.Column(db.String(50))
    browser_plugins = db.Column(db.Text)
    # Add other fields for fingerprinting if needed

    def __repr__(self):
        return f'<Hook {self.id}>'