from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence
from functools import cache
import json
import os

#DATABASE_URI = "postgresql+psycopg2://root:heslo1234@uo_database:5432/data"

def GetBaseSession(engineToBind):
    baseS = sessionmaker(bind = engineToBind)
    return baseS

def GetSession():
    newSession = BaseSession()
    return newSession

def GetEngine(URI):
    newEngine = create_engine(URI)
    return newEngine

def GetURI():
    user = os.environ["POSTGRES_USER"]
    password = os.environ["POSTGRES_PASSWORD"]
    return "postgresql+psycopg2://" + user + ":" + password + "@database:5432/data"

@cache
def GetDeclarativeBase():
    return declarative_base()

@cache
def GetUnitedSequence(name):
    seqName = name + "_id_seq"
    unitedSequence = Sequence(seqName)
    return unitedSequence

DATABASE_URI = GetURI()

SQLBase = GetDeclarativeBase()
engine = GetEngine(DATABASE_URI)
BaseSession = GetBaseSession(engine)