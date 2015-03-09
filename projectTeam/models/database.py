# -*- coding: UTF-8 -*- 

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from math import  ceil
from projectTeam.powerteamconfig import *

engine = create_engine(DB,echo=DEBUG)

BaseModel = declarative_base()

def get_session():
    return Session(bind = engine)

def pager(query,orderby,page_no,page_size=PAGESIZE):
    row_count = query.count()
    page_count = int(ceil(row_count * 1.0 / page_size))
    if page_no < 1:
        page_no = 1
    if page_no > page_count:
        page_no = page_count
    if page_no == 0:
        page_no = 1
        page_count = 1
    print '----------------------------'+orderby+'----------------------------'
    data = query.order_by(orderby).limit(page_size).offset((page_no - 1) * page_size)
    return (row_count,page_count,page_no,page_size,data)

def drop_database():
    BaseModel.metadata.drop_all(bind=engine)

def create_database():
    BaseModel.metadata.create_all(bind=engine)
    
    
  