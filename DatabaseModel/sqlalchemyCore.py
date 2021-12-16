from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence
from functools import cache

DATABASE_URI = "postgresql+psycopg2://postgres:password@host.docker.internal:5432/data"

def GetBaseSession(engineToBind):
    baseS = sessionmaker(bind = engineToBind)
    return baseS

def GetSession():
    newSession = BaseSession()
    return newSession

def GetEngine(URI):
    newEngine = create_engine(URI)
    return newEngine

@cache
def GetDeclarativeBase():
    return declarative_base()

@cache
def GetUnitedSequence(name):
    seqName = name + "_id_seq"
    unitedSequence = Sequence(seqName)
    return unitedSequence

SQLBase = GetDeclarativeBase()
engine = GetEngine(DATABASE_URI)
BaseSession = GetBaseSession(engine)