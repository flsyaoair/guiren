from projectTeam.models.database import BaseModel
from projectTeam.models.userprofile import UserProfile

from sqlalchemy import Column,DateTime,NVARCHAR,SMALLINT,Integer,ForeignKey, Float, UnicodeText
from sqlalchemy.orm import relationship

class TaskPriority:
    High = 1
    Middle = 2
    Low = 3

class TaskStatus:
    New = 1
    InProgress = 2
    Completed = 3
    Canceled = 4

class Task(BaseModel):

    __tablename__ = 'Task'
    TaskId = Column('TaskId', Integer,primary_key=True,nullable=False,autoincrement=True)
    ProjectId = Column('ProjectId', Integer,ForeignKey('Project.ProjectId'),nullable = False)
    TaskName = Column('TaskName', NVARCHAR(30),nullable = False)
    Priority = Column('Priority', SMALLINT,nullable=False)
    Progress = Column('Progress', SMALLINT,nullable=False)
    AssignTo = Column('AssignTo', Integer,ForeignKey('UserProfile.UserId'),nullable = False)
    AssignToProfile = relationship('UserProfile', foreign_keys=AssignTo,primaryjoin=AssignTo == UserProfile.UserId)
    Status = Column('Status', SMALLINT,nullable = False)
    Effort = Column('Effort', Float,nullable=False)
    Description = Column('Description', UnicodeText)
    Creator = Column('Creator', Integer,ForeignKey('UserProfile.UserId'),nullable = False)
    CreatorProfile = relationship('UserProfile', foreign_keys=Creator,primaryjoin=Creator == UserProfile.UserId)
    CreateDate = Column('CreateDate', DateTime,nullable=False)
    LastUpdateDate = Column('LastUpdateDate', DateTime,nullable=False)