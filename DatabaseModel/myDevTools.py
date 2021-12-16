from DatabaseModel.sqlalchemyCore import SQLBase, engine

def ClearMetadata():
    SQLBase.metadata.drop_all(engine)

def CreateMetadata():
    SQLBase.metadata.create_all(engine)

def AddToSessionAndCommit(object, session):
    session.add(object)
    session.commit()

def AddToSession(object, session):
    session.add(object)

def CommitSession(session):
    session.commit()

def CloseSession(session):
    session.close()
