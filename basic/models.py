from basic import db, login_manager, app #import our database and login_manager and app from basic.py
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

#reloading the user from user id stored in the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



############# user models that define with classes ################
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique= True, nullable=False)
    email = db.Column(db.String(120), unique= True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    #create methods to make a token
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec) #create token with Serializer
        return s.dumps({'user_id': self.id }).decode('utf-8') #return that token

    #create method to verity the token that we make
    #static method without self, using decorator, not expect any parameter as a self
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)



    #how our object is printed by using this methods
    def __repr__(self):
        return f"User('{self.username}','{self.email}')"

#--Rashmi
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    payment_id = db.Column(db.String(80), unique= True, nullable=False)
    order_id = db.Column(db.String(80))
    # user_id = db.Column(db.Integer)
    # username = db.Column(db.String(20), unique= True, nullable=False)
    order_amount = db.Column(db.Integer)
    plan_name = db.Column(db.String(80))
    # email = db.Column(db.String(120)
