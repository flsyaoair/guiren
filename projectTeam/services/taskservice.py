# -*- coding: UTF-8 -*-

from projectTeam.models import Task, TaskStatus, UserProfile, database, Member
from projectTeam.models.task import Task, TaskStatus,  TaskHistory
from datetime import datetime
from sqlalchemy.orm import joinedload
from projectTeam.powerteamconfig import *
from projectTeam.models.project import Project
from sqlalchemy import func
from projectTeam.services import userservice, mailservice
from math import  ceil
from projectTeam.models.comment import Comment, SubComment

def create(project_id,task_name,version,priority,assign_to,description,creator):
    session = database.get_session()
    task_name = task_name.strip()
    version =version.strip()
    t = Task()
    t.ProjectId = project_id
    t.TaskName = task_name
    t.Versions = version
    t.Priority = priority
    t.Progress = 0
    if assign_to == -1:
        t.AssignTo = creator
    else:
        t.AssignTo = assign_to
    assign_to = t.AssignTo
    t.Effort = 0
    t.Status = TaskStatus.New
    t.Description = description
    t.Creator = creator
    t.CreateDate = datetime.now()
    t.LastUpdateDate = datetime.now()
    
    session.add(t)
    session.commit()
    session.close()

    calcprogress(project_id)

    if ENABLE_MAIL_NOTICE:
        u = userservice.get_user_by_id(assign_to)
        body = mailservice.render_mail_template('Task/NoticeAssignTo.html',TaskName=task_name,Description=description,SystemUrl=HOST)
        mailservice.send_mail(u.Email, u'指派给您的新任务 ' + task_name,body)

def query(task_name,project_id,assign_to,status_new,status_in_progress,status_completed,status_canceled,order_by,page_no,page_size,current_user):
    session = database.get_session()

    filters = []
    status = []

    task_name = task_name.strip()
    if len(task_name) > 0:
        filters.append(Task.TaskName.like('%' + task_name + '%'))
    if not project_id == 'all':
        filters.append(Task.ProjectId == project_id)    
    if not assign_to == 0:
        filters.append(Task.AssignTo == assign_to)
    if status_new:
        status.append(TaskStatus.New)
    if status_in_progress:
        status.append(TaskStatus.InProgress)
    if status_completed:
        status.append(TaskStatus.Completed)
    if status_canceled:
        status.append(TaskStatus.Canceled)
    if len(status) > 0:
        filters.append(Task.Status.in_(status))

    project_list = session.query(Member.ProjectId).filter(Member.UserId == current_user)
    q = session.query(Task).join(UserProfile,UserProfile.UserId == Task.Creator).join(UserProfile,UserProfile.UserId == Task.AssignTo).join(Project,Project.ProjectId == Task.ProjectId).filter(Task.ProjectId.in_(project_list))
    for f in filters:
        q = q.filter(f)
    (row_count,page_count,page_no,page_size,data) = database.pager(q,order_by,page_no,page_size)

    session.close()
    return (row_count,page_count,page_no,page_size,data) 

def get(task_id):
    session = database.get_session()

    task = session.query(Task).options(joinedload(Task.AssignToProfile),joinedload(Task.ProjectProfile),joinedload(Task.CreatorProfile)).filter(Task.TaskId == task_id).one()

    session.close()
    return task

def get_history(task_id):
    session = database.get_session()

    history_list = session.query(TaskHistory).options(joinedload(TaskHistory.RawAssignToProfile),joinedload(TaskHistory.NewAssignToProfile),joinedload(TaskHistory.CreatorProfile)).filter(TaskHistory.TaskId == task_id)
                  
    session.close()

    return history_list
    
def update(project_id,task_id,task_name,version,assign_to,priority,progress,status,feedback,current_user):
    session = database.get_session()

    task_name = task_name.strip()
    version =version.strip()
    task = session.query(Task).filter(Task.TaskId == task_id).one()
    
    changeAssignTo = not (task.AssignTo == assign_to)
    description = task.Description
    priority = int(priority)
    assign_to = int(assign_to)
    status = int(status)
    if (not task.Status == status) or (not task.Priority == priority) or (not task.AssignTo == assign_to) or (len(feedback) > 0):
        history = TaskHistory()
        history.ProjectId = task.ProjectId
        history.TaskId = task.TaskId
        history.Name = task_name
        history.Versions = task.Versions
        history.RawStatus = task.Status
        history.NewStatus = status
        history.RawPriority = task.Priority
        history.NewPriority = priority
        history.RawAssignTo = task.AssignTo
        history.NewAssignTo = assign_to
#        history.RawCategoryId = issue.CategoryId
#        history.NewCategoryId = category_id
        history.Feedback = feedback
        history.Creator = current_user
        history.CreateDate = datetime.now()

        session.add(history)
    task.TaskName = task_name
    task.Versions = version
    task.AssignTo = assign_to
    task.Priority = priority
    task.Progress = progress
    task.Status = status
#    task.Description = description
#    task.Effort = task.Effort + float(effort)
    task.LastUpdateDate = datetime.now()
    project_id = task.ProjectId
    session.commit()
    session.close()

    calcprogress(project_id)

    if ENABLE_MAIL_NOTICE and changeAssignTo:
        u = userservice.get_user_by_id(assign_to)
        body = mailservice.render_mail_template('Task/NoticeAssignTo.html',TaskName=task_name,Description=description,SystemUrl=HOST)
        mailservice.send_mail(u.Email, u'指派给您的新任务 ' + task_name,body)

    return True

def calcprogress(project_id):
    session = database.get_session()

    all_project_task = session.query(Task).filter(Task.ProjectId == project_id).count()
    if all_project_task == 0:
        all_project_task = 1
    complete_project_task = session.query(Task).filter(Task.ProjectId == project_id).filter(Task.Status.in_([TaskStatus.Completed,TaskStatus.Canceled])).count()

    session.query(Project).filter(Project.ProjectId == project_id).update({'Progress':(complete_project_task * 100.0 / all_project_task),'LastUpdateDate':datetime.now()})
    session.commit()
    session.close()
def delete(task_id):
    session = database.get_session()

    task = session.query(Task).filter(Task.TaskId == task_id).one()
    project_id = task.ProjectId
    session.query(TaskHistory).filter(TaskHistory.TaskId == task_id).delete()
    
    comment = session.query(Comment).filter(Comment.TaskId == task_id)
    for commentid in comment:
        session.query(SubComment).filter(SubComment.CommentId == commentid.CommentId).delete()
    
    session.query(Comment).filter(Comment.TaskId == task_id).delete()
    session.delete(task)
    session.commit()
    session.close()

    calcprogress(project_id)

def statistics(project_id):
    session = database.get_session()

    task_status = session.query(Task.Status,func.count(Task.Status)).filter(Task.ProjectId == project_id).group_by(Task.Status).all()
    task_priority = session.query(Task.Priority,func.count(Task.Priority)).filter(Task.ProjectId == project_id).group_by(Task.Priority).all()

    session.commit()
    session.close()

    return (task_status,task_priority)
    
def member_task(current_user):
    session = database.get_session()
    
    project_list = session.query(Member.ProjectId).filter(Member.UserId == current_user)
    task_list = session.query(Task).filter(Task.ProjectId.in_(project_list)).all()
    
    return (task_list)
