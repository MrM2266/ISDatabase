from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey
from sqlalchemy.ext import declarative

engine = create_engine('sqlite:///code.db', echo = True)
Session = sessionmaker(bind = engine)
Base = declarative_base()

person_teaches = Table("person_lesson", Base.metadata,
                        Column("person_id", Integer, ForeignKey('people.id')),
                        Column("lesson_id", Integer, ForeignKey('lessons.id')))

class person(Base):
    __tablename__ = "people"
    
    id = Column(Integer, primary_key = True)
    name = Column(String)
    surname = Column(String)
    address = Column(String)
    lessons = relationship("lesson", secondary = person_teaches)
    
    def __init__(self, name, surname, address):
        self.name = name
        self.surname = surname
        self.address = address
        
def lesson(Base):
    __tablename__ = "lessons"
    
    id = Column(Integer, primary_key = True)
    date = Column(Date)
    topic = Column(String)
    
    def __init__(self, date, topic):
        self.date = date
        self.topic = topic