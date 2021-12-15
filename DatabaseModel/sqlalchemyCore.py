from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence

from functools import cache


def GetBaseSession(engineToBind):
    baseS = sessionmaker(bind = engineToBind)
    return baseS

def GetSession(BaseSession):
    newSession = BaseSession()
    return newSession

def GetEngine(URI):
    newEngine = create_engine(URI)
    return newEngine

@cache
def GetDeclarativeBase():
    return declarative_base()

@cache
def GetUnitedSequence():
    unitedSequence = Sequence('all_id_seq')
    return unitedSequence

SQLBase = GetDeclarativeBase()
unitedSequence = GetUnitedSequence()