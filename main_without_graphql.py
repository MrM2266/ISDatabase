from DatabaseModel.sqlalchemyCore import GetSession
from DatabaseModel.myDevTools import *
from DatabaseModel import randomData
from DatabaseModel.models import PersonModel, LessonModel, StudentModel, ProgramModel, GroupModel, SubjectModel, SemesterModel, GroupTypeModel, LessonTypeModel, RoomModel, BuildingModel, AreaModel
#from DatabaseModel import sqlalchemyCore #přístup do modulu přes tečku


mySession = GetSession()

ClearMetadata()
CreateMetadata()


randomData.preloadData(mySession)
randomData.buildings(mySession)
randomData.lekce(mySession)


CloseSession(mySession)