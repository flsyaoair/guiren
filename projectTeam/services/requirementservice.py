# -*- coding: UTF-8 -*-

from projectTeam.models import database
from projectTeam.models.requirement import Requirement, RequirementStatus
from datetime import datetime
from sqlalchemy.orm import joinedload
from projectTeam.powerteamconfig import *
from projectTeam.models.project import Project
from sqlalchemy import func
from projectTeam.services import userservice, mailservice

def create(requirement_name,version,description,creator):
    session = database.get_session()
    requirement_name = requirement_name.strip()
    version =version.strip()
    r = Requirement()
    r.RequirementName = requirement_name
    r.Status = RequirementStatus.InProgress
    r.Versions = version
    r.Status = RequirementStatus.New
    r.Description = description
    r.Creator = creator

    r.CreateDate = datetime.now()
    r.LastUpdateDate = datetime.now()
    
    session.add(r)
    session.commit()
    session.close()

   



def query(status):
    filters = []
    if not status == 'all':
        filters.append(Requirement.Status == status)
    session = database.get_session()
#    requirement_name = requirement_name.strip()
#    if len(requirement_name) > 0:
#        filters.append(Requirement.RequirementName.like('%' + requirement_name + '%'))
    requirementlist = session.query(Requirement).all()
    q=session.query(Requirement)
    for f in filters:
        requirementlist = q.filter(f)
    session.close()
    return  requirementlist

def get(requirement_id):
    
    session = database.get_session()

    requirementdetail = session.query(Requirement).options(joinedload(Requirement.CreatorProfile)).filter(Requirement.RequirementId==requirement_id).one()
    
    session.close()
    return  requirementdetail



def update(requirement_id, requirement_name, version, status, description,current_user):
    session = database.get_session()

    requirement_name = requirement_name.strip()
    version =version.strip()
    requirement = session.query(Requirement).filter(Requirement.RequirementId == requirement_id).one()

        
        
        
        

#    if (not requirement.Status == status) or (not requirement.RequirementName == requirement_name) or (len(feedback) > 0):
#        history = RequirementHistory()
#        history.TaskId = task.TaskId
#        history.RawStatus = task.Status
#        history.NewStatus = status
#        history.RawPriority = task.Priority
#        history.NewPriority = priority
#        history.RawAssignTo = task.AssignTo
#        history.NewAssignTo = assign_to
##        history.RawCategoryId = issue.CategoryId
##        history.NewCategoryId = category_id
#        history.Feedback = feedback
#        history.Creator = current_user
#        history.CreateDate = datetime.now()

#        session.add(history)
    requirement.RequirementName = requirement_name
    requirement.Versions = version

    requirement.Status = status
    requirement.Description = description
#    task.Effort = task.Effort + float(effort)
    requirement.LastUpdateDate = datetime.now()
 
    session.commit()
    session.close()

    return True
   
        

#def removerequirement(requirement_id):
#    session = database.get_session()
#    requirement = session.query(Requirement).filter(Requirement.RequirementId == requirement_id).one()
#    session.delete(requirement)
#    session.commit()
#    session.close()
#    return True
#


#def statistics(project_id):
#    session = database.get_session()
#
#    task_status = session.query(Task.Status,func.count(Task.Status)).filter(Task.ProjectId == project_id).group_by(Task.Status).all()
#    task_priority = session.query(Task.Priority,func.count(Task.Priority)).filter(Task.ProjectId == project_id).group_by(Task.Priority).all()
#
#    session.commit()
#    session.close()
#
#    return (task_status,task_priority)