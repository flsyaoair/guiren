# -*- coding: utf-8 -*-
from projectTeam.models.database import BaseModel
from sqlalchemy import Column,DateTime,NVARCHAR,SMALLINT,Integer,ForeignKey,UnicodeText,VARCHAR
from sqlalchemy.orm import relationship

class Notice(BaseModel):

    __tablename__ = 'Notice'
    NoticeId = Column('NoticeId', Integer,primary_key=True,nullable=False,autoincrement=True)
    Content = Column('Content', UnicodeText)
    CreateDate = Column('CreateDate', DateTime,nullable=False)
