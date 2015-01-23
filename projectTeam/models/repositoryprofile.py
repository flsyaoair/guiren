# -*- coding: UTF-8 -*- 

from projectTeam.models.database import BaseModel
from sqlalchemy import Column,DateTime,NVARCHAR,SMALLINT,Integer,ForeignKey, Float, UnicodeText
from sqlalchemy.orm import relationship
#from projectTeam.models.repos import Repository




class RepositoryProfile(BaseModel):

    __tablename__ = 'RepositoryProfile'
    RepositoryCategoryId = Column('RepositoryCategoryId', Integer,primary_key=True,nullable=False,autoincrement=True)
    RepositoryCategoryName = Column('RepositoryCategoryName', NVARCHAR(10),nullable = False)
    
#    RepositoryId = Column('RepositoryId', Integer,ForeignKey('Repository.RepositoryId'),nullable = False)
#    Repository = relationship('Repository', foreign_keys=RepositoryId,primaryjoin=RepositoryId == Repository.RepositoryId)
#    Status = Column('Status', SMALLINT,nullable = False)


