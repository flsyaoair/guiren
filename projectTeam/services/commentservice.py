# -*- coding: utf-8 -*-
from projectTeam.models import Comment, database
from datetime import datetime


def create(content, task_id, issue_id, requirement_id, creator):
    session = database.get_session()
    c = Comment()
    c.Content = content.strip()
    c.TaskId = task_id
    c.IssueId = issue_id
    c.RequirementId = requirement_id
    c.Creator = creator
    c.CreateDate = datetime.now()
    
    session.add(c)
    session.commit()
    session.close()

def query(task_id):
    session = database.get_session()
    comments = session.query(Comment).order_by(Comment.CreateDate)
    session.close()
    return comments