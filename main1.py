from sqlalchemy import Sequence
from starlette.graphql import GraphQLApp

from DatabaseModel import models
from DatabaseModel.sqlalchemyCore import *
from DatabaseModel.myDevTools import *
from DatabaseModel import randomData
#from DatabaseModel import sqlalchemyCore #přístup do modulu přes tečku

from fastapi import FastAPI, Request
import graphqlapp

print("running from main")
DATABASE_URI = "postgresql+psycopg2://postgres:password@host.docker.internal:5432/data"

def buildApp(session):
    def prepareSession():#Session=Session): # default parameters are not allowed here
        """generator for creating db session encapsulated with try/except block and followed session.commit() / session.rollback()

        Returns
        -------
        generator
            contains just one item which is instance of Session (SQLAlchemy)
        """
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close() 
    app = FastAPI()
    graphqlapp.attachGraphQL(app, prepareSession)
    return app

unitedSequence = Sequence('all_id_seq')
engine = GetEngine(DATABASE_URI) #initEngine
BaseSession = GetBaseSession(engine)
SQLBase = GetDeclarativeBase()

PersonModel, LessonModel, StudentModel, ProgramModel, GroupModel, SubjectModel, SemesterModel, GroupTypeModel, LessonTypeModel, RoomModel, BuildingModel, AreaModel = models.defineRelations(SQLBase, unitedSequence)

mySession = GetSession(BaseSession) #initSession

ClearMetadata(SQLBase, engine)
CreateMetadata(SQLBase, engine)

randomData.preloadData(PersonModel, LessonModel, StudentModel, ProgramModel, GroupModel, SubjectModel, SemesterModel, GroupTypeModel, LessonTypeModel, RoomModel, BuildingModel, AreaModel, mySession)

CloseSession(mySession)

app = buildApp(mySession)