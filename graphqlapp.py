from datetime import datetime
from typing_extensions import Required
from sqlalchemy.sql.sqltypes import DATE
from graphene import ObjectType, String, Int, Field, ID, List, Date, DateTime, Mutation, Boolean
from graphene import Schema as GSchema

from starlette.graphql import GraphQLApp
import graphene

import DatabaseModel.models as Models

from contextlib import contextmanager

def attachGraphQL(app, sessionFunc, bindPoint='/gql'):
    """Attaches a Swagger endpoint to a FastAPI

    Parameters
    ----------
    app: FastAPI
        app to bind to
    prepareSession: lambda : session
        callable which returns a db session
    """
    assert callable(sessionFunc), "sessionFunc must be a function creating a session"

    session_scope = contextmanager(sessionFunc)
    PersonModel, LessonModel, StudentModel, ProgramModel, GroupModel, SubjectModel, SemesterModel, GroupTypeModel, LessonTypeModel, RoomModel, BuildingModel, AreaModel = Models.GetModels()

    def extractSession(info):
        return info.context.get('session')

    class Person(ObjectType):
        id = ID()
        name = String()
        surname = String()
        address = String()
        email = String()
        #NM - PERSON - LESSON
        lessons = List(lambda: Lesson)
        #1N - PERSON - STUDENT
        students = List(lambda: Student)

        #NM - GROUP - PERSON
        groups = List(lambda: Group)

        def resolve_lessons(parent, info):
            session = extractSession(info)
            personRecord = session.query(PersonModel).get(parent.id)
            return personRecord.lessons

        def resolve_students(parent, info):
            session = extractSession(info)
            personRecord = session.query(PersonModel).get(parent.id)
            return personRecord.students

        def resolve_groups(parent, info):
            session = extractSession(info)
            personRecord = session.query(PersonModel).get(parent.id)
            return personRecord.groups

    class Lesson(ObjectType):
        id = ID()
        date = Date()
        topic = String()
        #NM - PERSON - LESSON
        persons = List(Person)
        #1N - LESSONTYPE - LESSON
        lessontypes = List(lambda: LessonType)
        #1N - ROOM - LESSON
        rooms = List(lambda: Room)

        def resolve_persons(parent, info):
            session = extractSession(info)
            lessonRecord = session.query(LessonModel).get(parent.id)
            return lessonRecord.persons

        def resolve_lessontypes(parent, info):
            session = extractSession(info)
            lessonRecord = session.query(LessonModel).get(parent.id)
            return lessonRecord.lessontypes

        def resolve_rooms(parent, info):
            session = extractSession(info)
            lessonRecord = session.query(LessonModel).get(parent.id)
            return lessonRecord.rooms

    class Student(ObjectType):
        id = ID()
        #1N - PROGRAM - STUDENT
        programs = List(lambda: Program)
        #1N - PERSON - STUDENT
        persons = List(Person)

        def resolve_programs(parent, info):
            session = extractSession(info)
            studentRecord = session.query(StudentModel).get(parent.id)
            return studentRecord.programs

        def resolve_persons(parent, info):
            session = extractSession(info)
            studentRecord = session.query(StudentModel).get(parent.id)
            return studentRecord.persons


    class Program(ObjectType):
        id = ID()
        name = String()
        #1N - PROGRAM - STUDENT
        students = List(Student)
        #1N - PROGRAM - SUBJECT
        subjects = List(lambda: Subject)
        
        def resolve_students(parent, info):
            session = extractSession(info)
            programRecord = session.query(ProgramModel).get(parent.id)
            return programRecord.students

        def resolve_subjects(parent, info):
            session = extractSession(info)
            programRecord = session.query(ProgramModel).get(parent.id)
            return programRecord.subjects

    class Group(ObjectType):
        id = ID()
        name = String()
        #NM - GROUP - PERSON
        persons = List(Person)

        #1N - GROUPTYPE - GROUP
        grouptypes = List(lambda: GroupType)

        def resolve_persons(parent, info):
            session = extractSession(info)
            groupRecord = session.query(GroupModel).get(parent.id)
            return groupRecord.persons

        def resolve_grouptypes(parent, info):
            session = extractSession(info)
            groupRecord = session.query(GroupModel).get(parent.id)
            return groupRecord.grouptypes

    class Subject(ObjectType):
        id = ID()
        name = String()
        #1N - SUBJECT - LESSON
        lessons = List(Lesson)

        #1N - SEMESTER - SUBJECT
        semesters = List(lambda: Semester)

        def resolve_lessons(parent, info):
            session = extractSession(info)
            subjectRecord = session.query(SubjectModel).get(parent.id)
            return subjectRecord.lessons

        def resolve_semesters(parent, info):
            session = extractSession(info)
            subjectRecord = session.query(SubjectModel).get(parent.id)
            return subjectRecord.semesters

    class Semester(ObjectType):
        id = ID()
        name = String()
        year = Int()
        number = Int()
        #1N - SEMESTER - SUBJECT
        subjects = List(Subject)

        def resolve_subjects(parent, info):
            session = extractSession(info)
            semesterRecord = session.query(SemesterModel).get(parent.id)
            return semesterRecord.subjects

    class GroupType(ObjectType):
        id = ID()
        name = String()
        #1N - GROUPTYPE - GROUP
        groups = List(Group)

        def resolve_groups(parent, info):
            session = extractSession(info)
            grouptypeRecord = session.query(GroupTypeModel).get(parent.id)
            return grouptypeRecord.groups

    class LessonType(ObjectType):
        id = ID()
        name = String()
        #1N - LESSONTYPE - LESSON
        lessons = List(Lesson)

        def resolve_lessons(parent, info):
            session = extractSession(info)
            lessontypeRecord = session.query(LessonTypeModel).get(parent.id)
            return lessontypeRecord.lessons

    class Room(ObjectType):
        id = ID()
        name = String()
        #1N - ROOM - LESSON
        lessons = List(Lesson)

        #1N - BUILDING - ROOM
        buildings = List(lambda: Building)  # TŘEBA TADY 1 MÍSTNOST MŮŽE BÝT JENOM V JEDNÝ BUDOVĚ

        def resolve_lessons(parent, info):
            session = extractSession(info)
            roomRecord = session.query(RoomModel).get(parent.id)
            return roomRecord.lessons

        def resolve_buildings(parent, info):
            session = extractSession(info)
            roomRecord = session.query(RoomModel).get(parent.id)
            return roomRecord.buildings

    class Building(ObjectType):
        id = ID()
        name = String()
        #1N - BUILDING - ROOM
        rooms = List(Room)

        #1N - AREA - BUILDING
        areas = List(lambda: Area)

        def resolve_rooms(parent, info):
            session = extractSession(info)
            buildingRecord = session.query(BuildingModel).get(parent.id)
            return buildingRecord.rooms

    class Area(ObjectType):
        id = ID()
        name = String()
        #1N - AREA - BUILDING
        buildings = List(Building)

        def resolve_buildings(parent, info):
            session = extractSession(info)
            areaRecord = session.query(AreaModel).get(parent.id)
            return areaRecord.buildings

    """class Query(ObjectType):

        #user = Field(User, id=ID(required=True))
        #group = Field(Group, id=ID(required=False, default_value=None), name=String(required=False, default_value=None))
        person = Field(Person, id=ID(required=True))

        def resolve_person(root, info, id):
            session = extractSession(info)
            return session.query(PersonModel).get(id)

        def resolve_user(root, info, id):
            #return {'name': info.context.get('session'), 'id': id}
            #return {'name': info.context['session'], 'id': id}
            session = extractSession(info)
            return session.query(UserModel).get(id)
        
        def resolve_group(root, info, id=None, name=None):
            
            session = extractSession(info)
            if id is None:
                return session.query(GroupModel).filter(GroupModel.name == name).first()
            else:
                return session.query(GroupModel).get(id)"""

    """class Mutations(ObjectType):
        create_user = CreateUser.Field()
        update_user = UpdateUser.Field()"""


    class localSchema(graphene.Schema):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)

        def execute(self, *args, **kwargs):
            with session_scope() as session:
                if 'context' in kwargs:
                    newkwargs = {**kwargs, 'context': {**kwargs['context'], 'session': session}}
                else:
                    newkwargs = {**kwargs, 'context': {'session': session}}
                return super().execute(*args, **newkwargs)

        async def execute_async(self, *args, **kwargs):
            with session_scope() as session:
                if 'context' in kwargs:
                    newkwargs = {**kwargs, 'context': {**kwargs['context'], 'session': session}}
                else:
                    newkwargs = {**kwargs, 'context': {'session': session}}
                return await super().execute_async(*args, **newkwargs)


    graphql_app = GraphQLApp(schema=localSchema(query=Query, mutation=Mutations))
    app.add_route(bindPoint, graphql_app)

# ZEPTAT SE NA ROZDÍL MEZI 1N A MN PŘI ŘEŠENÍ RELACÍ V GRAPHQL
# JAK U PROMĚNNÝCH TAK U FUNKCÍ
# ZEPTAT SE NA ROZDÍL U FUNKCÍ(RESOLVE) A PROMĚNNÝCH MEZI 1->N A N->1