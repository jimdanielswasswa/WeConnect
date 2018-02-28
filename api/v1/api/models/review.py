from datetime import datetime

from api import db


class Review(db.Model):
    """Represents A Review Object."""
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True, index=True)
    comment = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey(
        'businesses.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

    def create(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        """"""
        return "<Comment : {}>".format(self.id)

    @staticmethod
    def get_review(id):
        review = Review.query.get(int(id))
        return review
    @staticmethod
    def get_review_details(review):
        return {'comment':review.comment, 'userId':review.user_id, 'businessId':review.business_id}

    @staticmethod
    def get_reviews():
        reviews = Review.query.all()
        return reviews
