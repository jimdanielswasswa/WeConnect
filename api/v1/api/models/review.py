from datetime import datetime

class Review(object):
    id=0
    comment=''
    user_id=0
    business_id=0
    created_at = datetime.utcnow()
    updated_at = datetime.utcnow()

    def __init__(self,comment):
        self.comment = comment

def get_review(review):
    return {'comment':review.comment, 'userId':review.user_id, 'businessId':review.business_id}

def get_reviews():
    review1 = Review(comment='Nice!!')
    review2 = Review(comment='Greate!!')
    review1.id = 1
    review1.user_id = 1
    review1.business_id = 1,
    review2.id = 2
    review2.user_id = 2
    review2.business_id = 2,
    reviews = [ review1, review2 ]
    return reviews
