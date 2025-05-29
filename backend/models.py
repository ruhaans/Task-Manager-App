from app import db

class User(db.Model):
    __tablename__='users'

    id=db.Column(db.Integer, primary_key=True)
    username= db.Column (db.String(80), unique=True, nullable=False)
    email= db.Column (db.String(120), unique=True, nullable=False)
    password= db.Column (db.String(200), nullable=False)

    tasks= db.relationship('Task', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"


class Category(db.Model):
    __tablename__ = 'categories'

    id= db.Column (db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    tasks=db.relationship('Task', backref='category', lazy=True)

    def __repr__(self):
        return f"<Category {self.name}>"


class Task(db.Model):
    __tablename__  = 'tasks'

    id= db.Column (db.Integer, primary_key= True)
    title= db.Column (db.String(120), nullable=False)
    description= db.Column (db.Text)
    due_date= db.Column (db.Date)
    is_completed= db.Column (db.Boolean, default=False)

    user_id= db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    category_id=  db.Column ( db.Integer, db.ForeignKey('categories.id'), nullable=True)

    def __repr__(self):
        return f"<Task {self.title}>"
