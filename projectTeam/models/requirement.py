from projectTeam.models.database import BaseModel
from projectTeam.models.userprofile import UserProfile 
from projectTeam.models.project import Project 

from sqlalchemy import Column,DateTime,NVARCHAR,SMALLINT,Integer,ForeignKey, Float, UnicodeText, VARCHAR
from sqlalchemy.orm import relationship


class RequirementStatus:
    New = 1
    InProgress = 2
    Completed = 3
    Canceled = 4


class Requirement(BaseModel):

    __tablename__ = 'Requirement'
    RequirementId = Column('RequirementId', Integer,primary_key=True,nullable=False,autoincrement=True)
    RequirementName = Column('RequirementName', NVARCHAR(30),nullable = False)
    Versions = Column('Versions', NVARCHAR(30),nullable = False)
    Status = Column('Status', SMALLINT,nullable = False)
    Description = Column('Description', UnicodeText)
    CreateDate = Column('CreateDate', DateTime,nullable=False)
    LastUpdateDate = Column('LastUpdateDate', DateTime,nullable=False)

