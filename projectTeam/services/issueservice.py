# -*- coding: UTF-8 -*-
from projectTeam.models import database, Member
from projectTeam.models.issue import Issue, IssueStatus, IssueCategory, IssueCategoryStatus, IssueHistory
from projectTeam.models.userprofile import UserProfile
from projectTeam.powerteamconfig import *
from datetime import datetime
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from projectTeam.services import userservice, mailservice
from math import  ceil
from projectTeam.models.comment import Comment, SubComment

def create(project_id,subject,priority,assign_to,description,category_id,creator):
    session = database.get_session()
    subject = subject.strip()
    issue = Issue()
    issue.ProjectId = project_id
    issue.CategoryId = category_id
    issue.Subject = subject
    issue.Priority = priority
    issue.Description = description
    issue.Status = IssueStatus.Open
    if int(assign_to) == -1:
        issue.AssignTo = creator
    else:
        issue.AssignTo = assign_to
    assign_to=issue.AssignTo
    issue.Creator = creator
    issue.CreateDate = datetime.now()
    issue.LastUpdateDate = datetime.now()

    session.add(issue)
    session.commit()
    session.close()

    if ENABLE_MAIL_NOTICE:
        u = userservice.get_user_by_id(assign_to)
        body = mailservice.render_mail_template('Issue/NoticeAssignTo.html',Subject=subject,Description=description,SystemUrl=HOST)
        mailservice.send_mail(u.Email, u'指派给您的新问题 ' + subject,body)

def available_category():
    session = database.get_session()

    list = session.query(IssueCategory).filter(IssueCategory.Status == IssueCategoryStatus.Enabled).all()
    session.close()
    return list

def all_category():
    session = database.get_session()

    list = session.query(IssueCategory).all()
    session.close()
    return list

def query(subject,assign_to,category_id,status_open,status_fixed,status_closed,status_canceled,order_by,page_no,page_size,current_user):
    session = database.get_session()

    filters = []
    status = []

    subject = subject.strip()
    if len(subject) > 0:
        filters.append(Issue.Subject.like('%' + subject + '%'))
    if not assign_to == 0:
        filters.append(Issue.AssignTo == assign_to)
    if not category_id == -1:
        filters.append(Issue.CategoryId == category_id)
    if status_open:
        status.append(IssueStatus.Open)
    if status_fixed:
        status.append(IssueStatus.Fixed)
    if status_closed:
        status.append(IssueStatus.Closed)
    if status_canceled:
        status.append(IssueStatus.Canceled)
    if len(status) > 0:
        filters.append(Issue.Status.in_(status))

    project_list = session.query(Member.ProjectId).filter(Member.UserId == current_user)
    q = session.query(Issue).join(UserProfile,UserProfile.UserId == Issue.Creator).join(UserProfile,UserProfile.UserId == Issue.AssignTo).filter(Issue.ProjectId.in_(project_list))
    for f in filters:
        q = q.filter(f)
    (row_count,page_count,page_no,page_size,data) = database.pager(q,order_by,page_no,page_size)

    session.close()
    return (row_count,page_count,page_no,page_size,data) 

def get(issue_id):
    session = database.get_session()

    issue = session.query(Issue).options(joinedload(Issue.CreatorProfile),joinedload(Issue.AssignToProfile),joinedload(Issue.Category)).filter(Issue.IssueId == issue_id).one()

    session.close()
    return issue

def get_history(issue_id):
    session = database.get_session()

    history_list = session.query(IssueHistory).options(joinedload(IssueHistory.RawAssignToProfile),joinedload(IssueHistory.NewAssignToProfile),joinedload(IssueHistory.CreatorProfile),joinedload(IssueHistory.RawIssueCategory),joinedload(IssueHistory.NewIssueCategory)).filter(IssueHistory.IssueId == issue_id)

    session.close()

    return history_list

def update(project_id,issue_id,subject,category_id,assign_to,priority,status,feedback,current_user):
    session = database.get_session()
    subject = subject.strip()
    issue = session.query(Issue).filter(Issue.IssueId == issue_id).one()
    changeAssignTo = not (issue.AssignTo == assign_to)
    description = issue.Description
    category_id = int(category_id)
    assign_to = int(assign_to)
    priority = int(priority)
    status = int(status)
    
    if (not issue.Subject == subject) or (not issue.CategoryId == category_id) or (not issue.Status == status) or (not issue.Priority == priority) or (not issue.AssignTo == assign_to) or (len(feedback) > 0):
        history = IssueHistory()
        history.ProjectId = issue.ProjectId
        history.IssueId = issue.IssueId
        history.Name = issue.Subject
        history.RawStatus = issue.Status
        history.NewStatus = status
        history.RawPriority = issue.Priority
        history.NewPriority = priority
        history.RawAssignTo = issue.AssignTo
        history.NewAssignTo = assign_to
        history.RawCategoryId = issue.CategoryId
        history.NewCategoryId = category_id
        history.Feedback = feedback
        history.Creator = current_user
        history.CreateDate = datetime.now()

        session.add(history)

    issue.Subject = subject
    issue.CategoryId = category_id
    issue.AssignTo = assign_to
    issue.Priority = priority
    issue.Status = status
    issue.LastUpdateDate = datetime.now()

    session.commit()
    session.close()

    if ENABLE_MAIL_NOTICE and changeAssignTo:
        u = userservice.get_user_by_id(assign_to)
        body = mailservice.render_mail_template('Issue/NoticeAssignTo.html',Subject=subject,Description=description,SystemUrl=HOST)
        mailservice.send_mail(u.Email, u'指派给您的新问题 ' + subject,body)

    return True

def delete(issue_id):
    session = database.get_session()

    comments = session.query(Comment).filter(Comment.IssueId == issue_id)
    for comment in comments:
        session.query(SubComment).filter(SubComment.CommentId == comment.CommentId).delete()
    
    session.query(Comment).filter(Comment.IssueId == issue_id).delete()
    session.query(IssueHistory).filter(IssueHistory.IssueId == issue_id).delete()
    session.query(Issue).filter(Issue.IssueId == issue_id).delete()
    
    session.commit()
    session.close()

def statistics(project_id):
    session = database.get_session()

    issue_status = session.query(Issue.Status,func.count(Issue.Status)).filter(Issue.ProjectId == project_id).group_by(Issue.Status).all()
    issue_priority = session.query(Issue.Priority,func.count(Issue.Priority)).filter(Issue.ProjectId == project_id).group_by(Issue.Priority).all()

    session.commit()
    session.close()

    return (issue_status,issue_priority)

def enable_category(categoryid):
    session = database.get_session()

    user = session.query(IssueCategory).filter(IssueCategory.CategoryId == categoryid).update({'Status':IssueCategoryStatus.Enabled})

    session.commit()
    session.close()

def disable_category(categoryid):
    session = database.get_session()

    user = session.query(IssueCategory).filter(IssueCategory.CategoryId == categoryid).update({'Status':IssueCategoryStatus.Disabled})

    session.commit()
    session.close()

def create_category(categoryname):
    session = database.get_session()

    c = IssueCategory()
    c.CategoryName = categoryname.strip()
    c.Status = IssueCategoryStatus.Enabled

    session.add(c)

    session.commit()
    session.close()

def exist_category(categoryname):
    session = database.get_session()

    c = session.query(IssueCategory).filter(IssueCategory.CategoryName == categoryname).count()

    session.close()

    return c > 0
    
def member_issue(current_user):
    session = database.get_session()
    
    project_list = session.query(Member.ProjectId).filter(Member.UserId == current_user)
    issue_list = session.query(Issue).filter(Issue.ProjectId.in_(project_list)).all()
    
    return (issue_list)