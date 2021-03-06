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
    SunItemId = Column('SunItemId', Integer,primary_key=True,nullable=False,autoincrement=True)
    SunItemName = Column('SunItemName', NVARCHAR(30),nullable = False)
#    ThemeItemName = Column('ThemeItemName', NVARCHAR(10),nullable = False)
    Description = Column('Description', UnicodeText)
    CreateDate = Column('CreateDate', DateTime,nullable=False)
    LastUpdateDate = Column('LastUpdateDate', DateTime,nullable=False)
    ThemeItemId = Column('ThemeItemId', Integer,ForeignKey('ThemeItem.ThemeItemId'),nullable = False)
    
 
