# -*- coding: UTF-8 -*- 

from projectTeam.models.database import BaseModel
from projectTeam.models.userprofile import UserProfile
from projectTeam.models.project import Project
from sqlalchemy import Column,Integer,ForeignKey, Integer
from sqlalchemy.orm import relationship

class Member(BaseModel):

    __tablename__ = 'Member'
    MemberId = Column('MemberId', Integer,primary_key=True,nullable=False,autoincrement=True)
    ProjectId = Column('ProjectId', Integer,ForeignKey('Project.ProjectId'),nullable = False)
    Project = relationship('Project', foreign_keys=ProjectId,primaryjoin=ProjectId == Project.ProjectId)
    UserId = Column('UserId', Integer,ForeignKey('UserProfile.UserId'),nullable = False)
    User = relationship('UserProfile', foreign_keys=UserId,primaryjoin=UserId == UserProfile.UserId)