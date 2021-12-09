from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

def GetBaseSession(engineToBind):
    baseS = sessionmaker(bind = engineToBind)
    return baseS

def GetSession(BaseSession):
    newSession = BaseSession()
    return newSession

def GetEngine(URI):
    newEngine = create_engine(URI)
    return newEngine

def GetDeclarativeBase():
    return declarative_base()
