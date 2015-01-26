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

#def create_repository(repositoryname):
#    session = database.get_session()
#
#    c = Repository()
#    c.RepositoryName = repositoryname.strip()
##    c.Status = IssueCategoryStatus.Enabled
#
#    session.add(c)
#
#    session.commit()
#    session.close()