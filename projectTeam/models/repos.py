# -*- coding: UTF-8 -*- 

from projectTeam.models.database import BaseModel
from sqlalchemy import Column,DateTime,NVARCHAR,SMALLINT,Integer,ForeignKey, Float, UnicodeText
from sqlalchemy.orm import relationship

#from projectTeam.models.project import Project
from projectTeam.models.repositoryprofile import RepositoryProfile



class Repository(BaseModel):

    __tablename__ = 'Repository'
    RepositoryId = Column('RepositoryId', Integer,primary_key=True,nullable=False,autoincrement=True)
    RepositoryName = Column('RepositoryName', NVARCHAR(30),nullable = False)
#    Repositories = relationship("RepositoryProfile")
#    RepositoryCategoryId = Column('RepositoryCategoryId', Integer,ForeignKey('RepositoryProfile.RepositoryCategoryId'),nullable = False)
    RepositoryCategory = relationship('RepositoryProfile')
#    TaskId = Column('TaskId', Integer,ForeignKey('Task.TaskId'),nullable = False)
#    Task = relationship('Task', foreign_keys=TaskId,primaryjoin=TaskId == Task.TaskId)
#    Status = Column('Status', SMALLINT,nullable = False)


