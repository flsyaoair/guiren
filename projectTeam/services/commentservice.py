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

def query(task_id,issue_id,requirement_id,order_by,page_no,page_size):
    session = database.get_session()
    if task_id != 0:
        comments = session.query(Comment).filter(Comment.TaskId == task_id)
    if issue_id != 0:
        comments = session.query(Comment).filter(Comment.IssueId == issue_id)
    if requirement_id != 0:
        comments = session.query(Comment).filter(Comment.RequirementId == requirement_id)
    (row_count,page_count,page_no,page_size,comments) = database.pager_more(comments,order_by,page_no,page_size)
    comments_list = []
    for comment in comments.all():
        comments_list.append({'CommentId':comment.CommentId, 'Content':comment.Content, 'TaskId':comment.TaskId, 'IssueId':comment.IssueId, 'RequirementId':comment.RequirementId, 'Creator':comment.CreatorProfile.Nick, 'CreatorId':comment.Creator, 'CreateDate':comment.CreateDate.isoformat()})

    session.close()
    return (comments_list,row_count,page_count,page_no)