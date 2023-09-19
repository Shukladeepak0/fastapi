from ..Database.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer,primary_key=True, index=True)
    tittle = Column(String(255))
    body = Column(String(1000))
    user_id =Column(Integer, ForeignKey('users.id'))
    status = Column(String(255))

    creator = relationship("User", back_populates="posts")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True, index=True)
    firstname = Column(String(255))
    lastname = Column(String(255))
    email = Column(String(255), unique=True)
    mobile = Column(String(255))
    gender = Column(String(255))
    password = Column(String(255))
    status = Column(String(255))
    profilepic = Column(String(255))

    posts = relationship("Post", back_populates="creator")
