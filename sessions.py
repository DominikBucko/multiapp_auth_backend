from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.usermodel import User
from models.appmodel import Application

engine = create_engine('sqlite:///user.db', echo=True)
sessionFactory = sessionmaker(bind=engine)


class UserAlreadyExistsException(Exception):
    pass


class AppAlreadyExistsException(Exception):
    pass


def register(email, password):
    session = sessionFactory()

    if retrieve_user(email):
        raise UserAlreadyExistsException

    user = User(email, password)
    session.add(user)
    session.commit()


def retrieve_user(email):
    session = sessionFactory()
    return session.query(User).get(email)


def update_user(user):
    session = sessionFactory()
    session.add(user)
    session.commit()


def retrieve_app(name):
    session = sessionFactory()
    return session.query(Application).get(name)


def register_app(name):
    session = sessionFactory()
    if retrieve_app(name):
        raise AppAlreadyExistsException

    app = Application(name)

    session.add(app)
    session.commit()
