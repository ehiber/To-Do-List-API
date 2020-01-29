from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    task = db.relationship('task')

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "username": self.username,
            }
    
    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(240), nullable=False)
    done = db.Column(db.Boolean, default= False)
    user = db.relationship('user')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Tasks (Label: %r, Done: %r>' % self.label , self.done

    def serialize(self):
        return {
            "label": self.label,
            "done": self.done
        }