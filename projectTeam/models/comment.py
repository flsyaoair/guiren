# -*- coding: utf-8 -*-
from projectTeam.models.database import BaseModel
from sqlalchemy import Column,DateTime,NVARCHAR,SMALLINT,Integer,ForeignKey,UnicodeText,VARCHAR
from sqlalchemy.orm import relationship
from projectTeam.models.task import Task
from projectTeam.models.issue import Issue
from projectTeam.models.requirement import Requirement
from projectTeam.models.userprofile import UserProfile

class Comment(BaseModel):

    __tablename__ = 'Comment'
    CommentId = Column('CommentId', Integer,primary_key=True,nullable=False,autoincrement=True)
    Content = Column('Content', UnicodeText)
    TaskId = Column('TaskId', Integer,ForeignKey('Task.TaskId'),nullable = False)
    TaskProfile = relationship('Task', foreign_keys=TaskId,primaryjoin=TaskId == Task.TaskId)
    IssueId = Column('IssueId', Integer,ForeignKey('Issue.IssueId'),nullable = False)
    IssueProfile = relationship('Issue', foreign_keys=IssueId,primaryjoin=IssueId == Issue.IssueId)
    RequirementId = Column('RequirementId', Integer,ForeignKey('Requirement.RequirementId'),nullable = False)
    RequirementProfile = relationship('Requirement', foreign_keys=RequirementId,primaryjoin=RequirementId == Requirement.RequirementId)
    Creator = Column('Creator', Integer,ForeignKey('UserProfile.UserId'),nullable = False)
    CreatorProfile = relationship('UserProfile', foreign_keys=Creator,primaryjoin=Creator == UserProfile.UserId)
    CreateDate = Column('CreateDate', DateTime,nullable=False)    