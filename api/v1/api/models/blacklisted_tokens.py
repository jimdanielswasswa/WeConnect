from datetime import datetime

from api import db


class BlacklistedToken(db.Model):
    """
    Represents Blacklisted JWT tokens
    """
    __tablename__ = 'blacklisted_tokens'

    id = db.Column(db.Integer, primary_key=True, index=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.now()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def check_blacklist(token):
        result = False
        res = BlacklistedToken.query.filter_by(token=str(token)).first()
        if res:
            result = True
        return result

    def __repr__(self):
        return '<BlacklistedToken: {0}'.format(self.token)
