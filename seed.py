from app import app
from models import db, User, Feedback


db.drop_all()
db.create_all()

u1 = User.register(
    username="cherry",
    password="large",
    email="cherry@gmail.com",
    first_name="jonathan",
    last_name="huth",
)

u2 = User.register(
    username="chocolate",
    password="small",
    email="chocolate@gmail.com",
    first_name="eric",
    last_name="cartman",
    
)

u3 = User.register(
    username="bob",
    password="bob",
    email="bob",
    first_name="bob",
    last_name="bob",
    
)

f1 = Feedback(
    title="bob",
    content="bob",
    username="bob"
)

db.session.add_all([u1, u2, u3, f1])
db.session.commit()