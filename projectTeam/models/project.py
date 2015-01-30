# -*- coding: UTF-8 -*- 
from projectTeam.models.database import BaseModel

from sqlalchemy import Column,DateTime,NVARCHAR,SMALLINT,Integer,ForeignKey,UnicodeText,VARCHAR
from sqlalchemy.orm import relationship

class ProjectStatus:
    InProgress = 1
    Completed = 2
    Canceled = 3

class Project(BaseModel):

    __tablename__ = 'Project'
    ProjectId = Column('ProjectId', Integer,primary_key=True,nullable=False,autoincrement=True)
    ProjectName = Column('ProjectName', NVARCHAR(30),nullable=False)
    Status = Column('Status', SMALLINT,nullable = False)
    Progress = Column('Progress', SMALLINT,nullable=False)
    Creator = Column('Creator', Integer,ForeignKey('UserProfile.UserId'),nullable = False)
    UserProfile = relationship("UserProfile")
    CreateDate = Column('CreateDate', DateTime,nullable=False)
    LastUpdateDate = Column('LastUpdateDate', DateTime,nullable=False)
    Members = relationship("Member")
    Introduction = Column('Introduction', UnicodeText)
    ProjectKey = Column('ProjectKey', VARCHAR(255),nullable=False,unique=True)