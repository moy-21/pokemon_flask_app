from app import db, login
from flask_login import UserMixin # IS ONLY FOR THE USER MODEL!!!!
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import CheckConstraint

class Deck(db.Model):
    poke_id = db.Column(db.Integer, db.ForeignKey('pokemon.poke_id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name =  db.Column(db.String)
    email =  db.Column(db.String, unique=True, index=True)
    password =  db.Column(db.String)
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    icon =  db.Column(db.Integer)
    pokemen = db.relationship('Pokemon',
        secondary = 'deck',
        backref = 'users',
        lazy = 'dynamic'
    )

    # should return a unique identifing string
    def __repr__(self):
        return f'<User: {self.email} | {self.id}>'

    # Human readbale ver of rpr
    def __str__(self):
        return f'<User: {self.email} | {self.first_name} {self.last_name}>'

    #salts and hashes our password to make it hard to steal
    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    # compares the user password to the password provided in the login form
    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)

    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email=data['email']
        self.password = self.hash_password(data['password'])
        self.icon = data['icon']

    def get_icon_url(self):
        r1 = 'https://res.cloudinary.com/dipcloqy3/image/upload/v1651867932/character3_eqvcd2.png'
        r2 = 'https://res.cloudinary.com/dipcloqy3/image/upload/v1651869917/character4_hcdgai.png'
        r3 = 'https://res.cloudinary.com/dipcloqy3/image/upload/v1651867932/character1_rn81i8.webp'
        if self.icon == 1:
            return r1
        elif self.icon == 2:
            return r2
        elif self.icon == 3:
            return r3
        else:
            return None

    def catch_poke(self, poke):
        self.pokemen.append(poke)
        db.session.commit()

        

    # save the user to the database
    def save(self):
        db.session.add(self) #adds the user to the db session
        db.session.commit() #save everythig in the session to the db

class Pokemon(db.Model):
    poke_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    hp =  db.Column(db.Integer)
    attack =  db.Column(db.Integer)
    base_ = db.Column(db.Integer)
    sprite = db.Column(db.String)
    defense =  db.Column(db.Integer)

    def __repr__(self):
        return f'<Pokemon: {self.poke_id}|{self.name}'

    def delete_poke(self):
        db.session.delete(self)
        db.session.commit()
    def save(self):
        db.session.add(self)
        db.session.commit()


    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    # SELECT * FROM user WHERE id = ???

