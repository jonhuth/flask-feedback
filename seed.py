from app import app
from models import db, User


db.drop_all()
db.create_all()

u1 = User(
    username="cherry",
    password="large",
    email="cherry@gmail.com",
    first_name="jonathan",
    last_name="huth",
)

u2 = User(
    username="chocolate",
    password="small",
    email="chocolate@gmail.com",
    first_name="eric",
    last_name="cartman",
    
)

db.session.add_all([u1, u2])
db.session.commit()