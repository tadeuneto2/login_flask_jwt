from . import db

#from passlib.hash import pbkdf2_sha256 as sha256
from passlib.hash import pbkdf2_sha256 as sha256


class Users(db.Model):

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean, default=True)
    role = db.Column(db.String, default='user')

    def salve_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'name': x.name,
                'email': x.email,
                'role': x.role
            }

        def __repr__(self):
            return '<User %r>' % Users

        return {'Users': list(map(lambda x: to_json(x), cls.query.all()))}

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)
