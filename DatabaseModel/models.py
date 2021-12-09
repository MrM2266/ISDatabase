from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, BigInteger, Integer, Date, ForeignKey, Sequence, Table
from DatabaseModel import relationsFunctions as relations

def CreateModels(Base, unitedSequence):
    class PersonModel(Base):
        __tablename__ = "people"
    
        id = Column(Integer, unitedSequence, primary_key = True, autoincrement=True)
        name = Column(String)
        surname = Column(String)
        address = Column(String)
        email = Column(String)
        #osoba je n studenty - může studovat více programů
    
        
    class LessonModel(Base):
        __tablename__ = "lessons"
    
        id = Column(Integer, unitedSequence, primary_key = True, autoincrement=True)
        date = Column(Date)
        topic = Column(String)
    
        def __init__(self, date, topic):
            self.date = date
            self.topic = topic
        
    class StudentModel(Base):
        __tablename__ = "students"
    
        id = Column(BigInteger, unitedSequence, primary_key = True, autoincrement=True)
    
    class ProgramModel(Base):
        __tablename__ = "programs"
    
        id = Column(Integer, unitedSequence, primary_key = True, autoincrement=True)
        name = Column(String)
    
    class GroupModel(Base):
        __tablename__ = "groups"
    
        id = Column(Integer, unitedSequence, primary_key = True, autoincrement=True)
        name = Column(String)

    class SubjectModel(Base):
        __tablename__ = "subjects"

        id = Column(Integer, unitedSequence, primary_key = True, autoincrement=True)
        name = Column(String)

    class SemesterModel(Base):
        __tablename__ = "semesters"

        id = Column(Integer, unitedSequence, primary_key = True, autoincrement=True)
        name = Column(String)
        year = Column(Integer)
        number = Column(Integer)

    class GroupTypeModel(Base):
        __tablename__ = "group_types"
        id = Column(Integer, unitedSequence, primary_key = True, autoincrement=True)

        name = Column(String)

    class LessonTypeModel(Base):
        __tablename__ = "lesson_types"
        id = Column(Integer, unitedSequence, primary_key = True, autoincrement=True)

        name = Column(String)

    class RoomModel(Base):
        __tablename__ = "rooms"
        id = Column(Integer, unitedSequence, primary_key = True, autoincrement=True)

        name = Column(String)

    class BuildingModel(Base):
        __tablename__ = "buildings"
        id = Column(Integer, unitedSequence, primary_key = True, autoincrement=True)

        name = Column(String)

    class AreaModel(Base):
        __tablename__ = "areas"
        id = Column(Integer, unitedSequence, primary_key = True, autoincrement=True)

        name = Column(String)


    return PersonModel, LessonModel, StudentModel, ProgramModel, GroupModel, SubjectModel, SemesterModel, GroupTypeModel, LessonTypeModel, RoomModel, BuildingModel, AreaModel


def defineRelations(Base, unitedSequence):
    PersonModel, LessonModel, StudentModel, ProgramModel, GroupModel, SubjectModel, SemesterModel, GroupTypeModel, LessonTypeModel, RoomModel, BuildingModel, AreaModel = CreateModels(Base, unitedSequence)
    relations.defineRelationNM(PersonModel, LessonModel) #teaches
    relations.defineRelation1N(ProgramModel, StudentModel)
    relations.defineRelation1N(PersonModel, StudentModel)
    relations.defineRelationNM(GroupModel, PersonModel)
    relations.defineRelation1N(ProgramModel, SubjectModel)
    relations.defineRelation1N(SubjectModel, LessonModel)
    relations.defineRelation1N(SemesterModel, SubjectModel)
    relations.defineRelation1N(LessonTypeModel, LessonModel)
    relations.defineRelation1N(GroupTypeModel, GroupModel)
    relations.defineRelation1N(RoomModel, LessonModel)
    relations.defineRelation1N(BuildingModel, RoomModel)
    relations.defineRelation1N(AreaModel, BuildingModel)


    return PersonModel, LessonModel, StudentModel, ProgramModel, GroupModel, SubjectModel, SemesterModel, GroupTypeModel, LessonTypeModel, RoomModel, BuildingModel, AreaModel
