from projectTeam.models.database import BaseModel
from projectTeam.models.userprofile import UserProfile 
from projectTeam.models.project import Project 

from sqlalchemy import Column,DateTime,NVARCHAR,SMALLINT,Integer,ForeignKey, Float, UnicodeText, VARCHAR
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

class TaskHistory(BaseModel):

    __tablename__ = 'TaskHistory'
    HistoryId = Column('HistoryId', Integer,primary_key=True,nullable=False,autoincrement=True)
    ProjectId = Column('ProjectId', Integer,ForeignKey('Project.ProjectId'),nullable = False)
    ProjectProfile = relationship('Project', lazy='subquery', foreign_keys=ProjectId,primaryjoin=ProjectId == Project.ProjectId)
    TaskId = Column('TaskId', Integer,ForeignKey('Task.TaskId'),nullable = False)
    Name = Column('Name', NVARCHAR(30),ForeignKey('Task.TaskName'),nullable = False)
    Versions = Column('Versions', NVARCHAR(30),ForeignKey('Task.Versions'),nullable = False)
    RawStatus = Column('RawStatus', SMALLINT,nullable = False)
    NewStatus = Column('NewStatus', SMALLINT,nullable = False)
    RawPriority = Column('RawPriority', SMALLINT,nullable = False)
    NewPriority = Column('NewPriority', SMALLINT,nullable = False)
    RawAssignTo = Column('RawAssignTo', Integer,ForeignKey('UserProfile.UserId'),nullable = False)
    RawAssignToProfile = relationship('UserProfile', foreign_keys=RawAssignTo,primaryjoin=RawAssignTo == UserProfile.UserId)
    NewAssignTo = Column('NewAssignTo', Integer,ForeignKey('UserProfile.UserId'),nullable = False)
    NewAssignToProfile = relationship('UserProfile', foreign_keys=NewAssignTo,primaryjoin=NewAssignTo == UserProfile.UserId)
#    RawCategoryId = Column('RawCategoryId', Integer,ForeignKey('IssueCategory.CategoryId'),nullable = False)
#    RawIssueCategory = relationship('IssueCategory', foreign_keys=RawCategoryId,primaryjoin=RawCategoryId == IssueCategory.CategoryId)
#    NewCategoryId = Column('NewCategoryId', Integer,ForeignKey('IssueCategory.CategoryId'),nullable = False)
#    NewIssueCategory = relationship('IssueCategory', foreign_keys=NewCategoryId,primaryjoin=NewCategoryId == IssueCategory.CategoryId)
    Feedback = Column('Feedback', UnicodeText)
    Creator = Column('Creator', Integer,ForeignKey('UserProfile.UserId'),nullable = False)
    CreatorProfile = relationship('UserProfile', foreign_keys=Creator,primaryjoin=Creator == UserProfile.UserId)
    CreateDate = Column('CreateDate', DateTime,nullable=False)



class Task(BaseModel):

    __tablename__ = 'Task'
    TaskId = Column('TaskId', Integer,primary_key=True,nullable=False,autoincrement=True)
    ProjectId = Column('ProjectId', Integer,ForeignKey('Project.ProjectId'),nullable = False)
    ProjectProfile = relationship('Project', foreign_keys=ProjectId,primaryjoin=ProjectId == Project.ProjectId)
    TaskName = Column('TaskName', NVARCHAR(30),nullable = False)
    Versions = Column('Versions', NVARCHAR(30),nullable = False)
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

    