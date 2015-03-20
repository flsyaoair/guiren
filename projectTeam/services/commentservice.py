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
    
    comment_id = session.query(Comment).order_by(Comment.CreateDate.desc()).first().CommentId
    return comment_id

def query(task_id,order_by,page_no,page_size):
    session = database.get_session()
    comments = session.query(Comment).filter(Comment.TaskId == task_id)
    (row_count,page_count,page_no,page_size,comments) = database.pager_more(comments,order_by,page_no,page_size)
    session.close()
    return (comments,row_count,page_count,page_no)