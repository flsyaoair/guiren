# -*- coding: UTF-8 -*-
from projectTeam.models import database
#from projectTeam.models.issue import Issue, IssueStatus, IssueCategory, IssueCategoryStatus, IssueHistory
from projectTeam.models.repos import Repository
from projectTeam.models.userprofile import UserProfile
from projectTeam.powerteamconfig import *
from datetime import datetime
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from projectTeam.services import userservice, mailservice

def create_repository(repositoryname):
    session = database.get_session()

    c = Repository()
    c.RepositoryName = repositoryname.strip()
#    c.Status = IssueCategoryStatus.Enabled

    session.add(c)

    session.commit()
    session.close()
    
def exist_repository(repositoryname):
    session = database.get_session()

    c = session.query(Repository).filter(Repository.RepositoryName == repositoryname).count()

    session.close()

    return c > 0
def query_repository():
    
    session = database.get_session()

    list = session.query(Repository).all()
    session.close()
    return list
#    filters=[]
#    
#    session = database.get_session()
#
#    if len(repositoryname) > 0:
#        filters.append(Repository.RepositoryName.like('%' + repositoryname + '%'))
##    if not status == '-1':
##        filters.append(Repository.Status == status)
#    R = session.query(Repository).filter(Repository.RepositoryId.in_(project_list))
#    for f in filters:
#        R = R.filter(f)
#
#    (row_count,page_count,page_no,page_size,data) = database.pager(R,order_by,page_no,PAGESIZE)
#    session.close()
#
#    return (row_count,page_count,page_no,page_size,data)

    