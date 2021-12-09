from sqlalchemy import Sequence

from DatabaseModel import models
from DatabaseModel.sqlalchemyCore import *
from DatabaseModel.myDevTools import *
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

studentsGroup = GroupModel(name = "Studenti_UO")
teachersGroup = GroupModel(name = "ucitele")
departmentGroup = GroupModel(name = "K-209")
adam = PersonModel(name = "Adam", surname = "Novotny", address = "Brno", email = "adam@unob.cz")
petr = PersonModel(name = "Petr", surname = "Veliky", address = "Petrohrad", email = "petr@unob.cz")
studentsGroup.people.append(petr)
adam.groups.append(teachersGroup)
petr.groups.append(departmentGroup)

area1 = AreaModel(name = "Kasarna Sumavska")
area2 = AreaModel(name = "Kasarna Jana Babaka")
building1 = BuildingModel(name = "jidelna")
building2 = BuildingModel(name = "Katedra Informatiky")
building3 = BuildingModel(name = "Brana KJB")


area1.buildings.append(building1)
area1.buildings.append(building2)
area2.buildings.append(building3)

AddToSession(adam, mySession)
AddToSession(studentsGroup, mySession)
AddToSession(area1, mySession)
AddToSession(area2, mySession)
AddToSession(building1, mySession)
AddToSession(building2, mySession)
AddToSession(building3, mySession)
CommitSession(mySession)

CloseSession(mySession)