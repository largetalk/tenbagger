import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import Sequence
from sqlalchemy.orm import sessionmaker

from settings import db_url


engine = create_engine(db_url, echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'

     id = Column(Integer, primary_key=True)
     id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
     name = Column(String)
     fullname = Column(String)
     password = Column(String)

     def __repr__(self):
         return "<User(name='%s', fullname='%s', password='%s')>" % (
             self.name, self.fullname, self.password)

def create_table():
    Base.metadata.create_all(engine)

def create_session():
    session = Session()
    return session

def test():
    session = create_session()
    ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
    session.add(ed_user) #insert
    our_user = session.query(User).filter_by(name='ed').first() #select
    session.add_all([
        User(name='wendy', fullname='Wendy Williams', password='foobar'),
        User(name='mary', fullname='Mary Contrary', password='xxg527'),
        User(name='fred', fullname='Fred Flinstone', password='blah')]) # insert a lot
    
    ed_user.password = 'f8s7ccs'
    session.dirty #IdentitySet([<User(name='ed', fullname='Ed Jones', password='f8s7ccs')>])
    session.new  #IdentitySet([<User(name='wendy', fullname='Wendy Williams', password='foobar')>,...
    session.commit() # commit
    session.rollback() # rollback
