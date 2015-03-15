# -*- coding: UTF-8 -*- 

from projectTeam.models.database import BaseModel
from sqlalchemy import Column,DateTime,NVARCHAR,SMALLINT,Integer,ForeignKey, Float, UnicodeText
from sqlalchemy.orm import relationship
#from projectTeam.models.repos import Repository




class ThemeItem(BaseModel):

    __tablename__ = 'ThemeItem'
    ThemeItemId = Column('ThemeItemId', Integer,primary_key=True,nullable=False,autoincrement=True)
    ThemeItemName = Column('ThemeItemName', NVARCHAR(10),nullable = False)
    Sunitem = relationship('SunItem')
class SunItem(BaseModel):

    __tablename__ = 'SunItem'
    RequirementId = Column('SunItemId', Integer,primary_key=True,nullable=False,autoincrement=True)
    RequirementName = Column('SunItemName', NVARCHAR(30),nullable = False)
    Description = Column('Description', UnicodeText)
    CreateDate = Column('CreateDate', DateTime,nullable=False)
    LastUpdateDate = Column('LastUpdateDate', DateTime,nullable=False)
    ThemeItemId = Column('ThemeItemIdId', Integer,ForeignKey('ThemeItemId.ThemeItemIdId'),nullable = False)
    
 
