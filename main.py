from starlette.graphql import GraphQLApp

from DatabaseModel.sqlalchemyCore import GetSession
from DatabaseModel.myDevTools import *
from DatabaseModel import randomData
from DatabaseModel.models import PersonModel, LessonModel, StudentModel, ProgramModel, GroupModel, SubjectModel, SemesterModel, GroupTypeModel, LessonTypeModel, RoomModel, BuildingModel, AreaModel

from fastapi import FastAPI
import graphqlapp


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



mySession = GetSession()

ClearMetadata()
CreateMetadata()
randomData.preloadData(mySession)
randomData.buildings(mySession)
randomData.lekce(mySession)

CloseSession(mySession)

gqlSession = GetSession()
app = buildApp(gqlSession)
CloseSession(gqlSession)