# -*- coding: UTF-8 -*- 

from projectTeam.models.database import BaseModel
from sqlalchemy import Column,DateTime,NVARCHAR,SMALLINT,Integer,ForeignKey, Float, UnicodeText
from sqlalchemy.orm import relationship
from projectTeam.models.userprofile import UserProfile
from projectTeam.models.project import Project 

class IssueStatus:
    Open = 1
    Fixed = 2
    Closed = 3
    Canceled = 4

class IssueCategoryStatus:
    Enabled = 1
    Disabled = 2

class IssuePriority:
    High = 1
    Middle = 2
    Low = 3

class IssueCategory(BaseModel):

    __tablename__ = 'IssueCategory'
    CategoryId = Column('CategoryId', Integer,primary_key=True,nullable=False,autoincrement=True)
    CategoryName = Column('CategoryName', NVARCHAR(10),nullable = False)
    Status = Column('Status', SMALLINT,nullable = False)

class IssueHistory(BaseModel):

    __tablename__ = 'IssueHistory'
    HistoryId = Column('HistoryId', Integer,primary_key=True,nullable=False,autoincrement=True)
    ProjectId = Column('ProjectId', Integer,ForeignKey('Project.ProjectId'),nullable = False)
    ProjectProfile = relationship('Project', lazy='subquery', foreign_keys=ProjectId,primaryjoin=ProjectId == Project.ProjectId)
    IssueId = Column('IssueId', Integer,ForeignKey('Issue.IssueId'),nullable = False)
    Name = Column('Name', NVARCHAR(30),ForeignKey('Issue.Subject'),nullable = False)
    RawStatus = Column('RawStatus', SMALLINT,nullable = False)
    NewStatus = Column('NewStatus', SMALLINT,nullable = False)
    RawPriority = Column('RawPriority', SMALLINT,nullable = False)
    NewPriority = Column('NewPriority', SMALLINT,nullable = False)
    RawAssignTo = Column('RawAssignTo', Integer,ForeignKey('UserProfile.UserId'),nullable = False)
    RawAssignToProfile = relationship('UserProfile', foreign_keys=RawAssignTo,primaryjoin=RawAssignTo == UserProfile.UserId)
    NewAssignTo = Column('NewAssignTo', Integer,ForeignKey('UserProfile.UserId'),nullable = False)
    NewAssignToProfile = relationship('UserProfile', foreign_keys=NewAssignTo,primaryjoin=NewAssignTo == UserProfile.UserId)
    RawCategoryId = Column('RawCategoryId', Integer,ForeignKey('IssueCategory.CategoryId'),nullable = False)
    RawIssueCategory = relationship('IssueCategory', foreign_keys=RawCategoryId,primaryjoin=RawCategoryId == IssueCategory.CategoryId)
    NewCategoryId = Column('NewCategoryId', Integer,ForeignKey('IssueCategory.CategoryId'),nullable = False)
    NewIssueCategory = relationship('IssueCategory', foreign_keys=NewCategoryId,primaryjoin=NewCategoryId == IssueCategory.CategoryId)
    Feedback = Column('Feedback', UnicodeText)
    Creator = Column('Creator', Integer,ForeignKey('UserProfile.UserId'),nullable = False)
    CreatorProfile = relationship('UserProfile', foreign_keys=Creator,primaryjoin=Creator == UserProfile.UserId)
    CreateDate = Column('CreateDate', DateTime,nullable=False)

class Issue(BaseModel):

    __tablename__ = 'Issue'
    IssueId = Column('IssueId', Integer,primary_key=True,nullable=False,autoincrement=True)
    ProjectId = Column('ProjectId', Integer,ForeignKey('Project.ProjectId'),nullable = False)
    ProjectProfile = relationship('Project', lazy='subquery', foreign_keys=ProjectId,primaryjoin=ProjectId == Project.ProjectId)
    CategoryId = Column('CategoryId', Integer,ForeignKey('IssueCategory.CategoryId'),nullable = False)
    Category = relationship('IssueCategory', foreign_keys=CategoryId,primaryjoin=CategoryId == IssueCategory.CategoryId)
    Subject = Column('Subject', NVARCHAR(30),nullable = False)
    Description = Column('Description', UnicodeText)
    Priority = Column('Priority', SMALLINT,nullable=False)
    Status = Column('Status', SMALLINT,nullable = False)
    AssignTo = Column('AssignTo', Integer,ForeignKey('UserProfile.UserId'),nullable = False)
    AssignToProfile = relationship('UserProfile', foreign_keys=AssignTo,primaryjoin=AssignTo == UserProfile.UserId)
    Creator = Column('Creator', Integer,ForeignKey('UserProfile.UserId'),nullable = False)
    CreatorProfile = relationship('UserProfile', foreign_keys=Creator,primaryjoin=Creator == UserProfile.UserId)
    CreateDate = Column('CreateDate', DateTime,nullable=False)
    LastUpdateDate = Column('LastUpdateDate', DateTime,nullable=False)

#class IssueComment(BaseModel):

#    __tablename__ = 'IssueComment'
#    CommentId = Column('CommentId', Integer,primary_key=True,nullable=False,autoincrement=True)
#    Content = Column('Content', UnicodeText)
#    IssueId = Column('IssueId', Integer,ForeignKey('Issue.IssueId'),nullable = False)
#    IssueProfile = relationship('Issue', foreign_keys=IssueId,primaryjoin=IssueId == Issue.IssueId)
#    Creator = Column('Creator', Integer,ForeignKey('UserProfile.UserId'),nullable = False)
#    CreatorProfile = relationship('UserProfile', foreign_keys=Creator,primaryjoin=Creator == UserProfile.UserId)
#    CreateDate = Column('CreateDate', DateTime,nullable=False)