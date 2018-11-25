import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))
    print "user table is made"


class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='cascade'))
    user = relationship(User, cascade="save-update")

    print "user table is added to restaurant"

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {'name': self.name, 'id': self.id, }


class MenuItem(Base):
    __tablename__ = 'menu_item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id',
                                               ondelete='cascade'))
    restaurant = relationship(Restaurant,
                              backref=backref("items",
                                              cascade="all, delete-orphan"))
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    user = relationship(User, cascade="save-update")
    print "User added to menu"

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {'name': self.name, 'description': self.description,
                'id': self.id, 'price': self.price,
                'course': self.course, }


print "DB IS DONE"
engine = create_engine('sqlite:///myNewRestaurantsWithUsersBB.db')
Base.metadata.create_all(engine)
