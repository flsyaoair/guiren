# -*- coding: UTF-8 -*-

from projectTeam.models import database
from projectTeam.models.item import SunItem,ThemeItem
from datetime import datetime
from sqlalchemy.orm import joinedload
from projectTeam.powerteamconfig import *
from projectTeam.models.project import Project
from sqlalchemy import func
from projectTeam.services import userservice, mailservice

def create_ThemeItem(ThemeItem_name,creator):
    session = database.get_session()
    ThemeItem_name = ThemeItem_name.strip()
    T=ThemeItem()
    T.ThemeItemName = ThemeItem_name
    session.add(T)
    session.commit()
    session.close()


def create(SunItem_name,ThemeItem_id,description,creator):
    session = database.get_session()
    sunItem_name =SunItem_name.strip() 
    I = SunItem()
    I.ThemeItemId = ThemeItem_id
    I.SunItemName = sunItem_name
    I.Description = description
    I.Creator = creator
    I.CreateDate = datetime.now()
    I.LastUpdateDate = datetime.now()
    session.add(I)
    session.commit()
    session.close()

def query_ThemeItem():
    
    session = database.get_session()

    list = session.query(ThemeItem).all()
    session.close()
    return list

#def query(status,page_no,order_by):
#    filters = []
#    if not status == 'all':
#        filters.append(Requirement.Status == status)
#    session = database.get_session()
#    requirementlist = session.query(Requirement)
#    q=session.query(Requirement)
#    for f in filters:
#        requirementlist = q.filter(f)
#    (row_count,page_count,page_no,page_size,data) = database.pager(requirementlist,order_by,page_no)
#    session.close()
#    return  (row_count,page_count,page_no,page_size,data)

def get(themeitemid):
    session = database.get_session()
    SunItemList = session.query(SunItem).filter(SunItem.ThemeItemId==themeitemid).one()
    session.close()
    return  SunItemList
#
#
#
#def update(requirement_id, requirement_name, version, status, description,current_user):
#    session = database.get_session()
#    requirement_name = requirement_name.strip()
#    version =version.strip()
#    requirement = session.query(Requirement).filter(Requirement.RequirementId == requirement_id).one()
#    requirement.RequirementName = requirement_name
#    requirement.Versions = version
#    requirement.Status = status
#    requirement.Description = description
#    requirement.LastUpdateDate = datetime.now()
#    session.commit()
#    session.close()
#    return True
   
        

