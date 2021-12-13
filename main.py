from sqlalchemy import Sequence

from DatabaseModel import models
from DatabaseModel.sqlalchemyCore import *
from DatabaseModel.myDevTools import *
from DatabaseModel import randomData
#from DatabaseModel import sqlalchemyCore #přístup do modulu přes tečku

print("running from main")
DATABASE_URI = "postgresql+psycopg2://postgres:password@host.docker.internal:5432/data"


unitedSequence = Sequence('all_id_seq')
engine = GetEngine(DATABASE_URI)
BaseSession = GetBaseSession(engine)
SQLBase = GetDeclarativeBase()

PersonModel, LessonModel, StudentModel, ProgramModel, GroupModel, SubjectModel, SemesterModel, GroupTypeModel, LessonTypeModel, RoomModel, BuildingModel, AreaModel = models.defineRelations(SQLBase, unitedSequence)

mySession = GetSession(BaseSession)

ClearMetadata(SQLBase, engine)
CreateMetadata(SQLBase, engine)
randomData.preloadData(PersonModel, LessonModel, StudentModel, ProgramModel, GroupModel, SubjectModel, SemesterModel, GroupTypeModel, LessonTypeModel, RoomModel, BuildingModel, AreaModel, mySession)

#vytvori dve oblasti a prida jim par budov
randomData.test1(PersonModel, LessonModel, StudentModel, ProgramModel, GroupModel, SubjectModel, SemesterModel, GroupTypeModel, LessonTypeModel, RoomModel, BuildingModel, AreaModel, mySession)


CloseSession(mySession)