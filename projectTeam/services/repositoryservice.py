# -*- coding: UTF-8 -*-
from projectTeam.models import database
#from projectTeam.models.issue import Issue, IssueStatus, IssueCategory, IssueCategoryStatus, IssueHistory
# from projectTeam.models.repos import Repository
from projectTeam.models.repositoryprofile import RepositoryProfile
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

def create_repositoryprofile(project_id,repositorycategory_name):
    session = database.get_session()
    r = RepositoryProfile()
    repositorycategory_name = repositorycategory_name.strip()
    r.ProjectId=project_id
    r.RepositoryCategoryName=repositorycategory_name
    r.CMPlatform = ''
    r.CIPlatform = ''
    r.ReposPlatform = ''
    session.add(r)
    session.commit()
    session.close()

    
def exist_repositoryprofile(project_id,repositorycategory_name):
    session = database.get_session()

    c = session.query(RepositoryProfile).filter(RepositoryProfile.RepositoryCategoryName == repositorycategory_name,RepositoryProfile.ProjectId == project_id).count()

    session.close()

    return c > 0    
def get(repository_id):
    
    session = database.get_session()

    r = session.query(Repository).filter(Repository.RepositoryId == repository_id).one()
    
    session.close()
    return r
def remove_Repository(repository_id):
    
    session = database.get_session()

    r1 = session.query(RepositoryProfile).filter(RepositoryProfile.RepositoryId == repository_id).delete()
    r2 = session.query(Repository).filter(Repository.RepositoryId == repository_id).delete()
    session.commit()
    session.close()
   
   
def query_repositoryprofile(project_id):
    
    session = database.get_session()

    list = session.query(RepositoryProfile).filter(RepositoryProfile.ProjectId == project_id)
    session.close()
    return list
def get_repositoryprofile(repositorycategory_id):
    
    session = database.get_session()

    list = session.query(RepositoryProfile).filter(RepositoryProfile.RepositoryCategoryId == repositorycategory_id)
    session.close()
    return list
#remove_Repository
def remove_RepositoryCategory(project_id,repositoryCategory_id):
    
    session = database.get_session()

    list = session.query(RepositoryProfile).filter(RepositoryProfile.ProjectId == project_id,RepositoryProfile.RepositoryCategoryId == repositoryCategory_id).delete()
    session.commit()
    session.close()
   
    return list

   