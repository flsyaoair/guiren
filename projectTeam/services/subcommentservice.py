# -*- coding: utf-8 -*-
from projectTeam.models import Comment, database
from projectTeam.models.comment import SubComment
from datetime import datetime

def create(content, comment_id, replyto, creator):
    session = database.get_session()
    subc = SubComment()
    subc.Content = content.strip()
    subc.CommentId = comment_id
    subc.ReplyTo = replyto
    subc.Creator = creator
    subc.CreateDate = datetime.now()
    
    session.add(subc)
    session.commit()
    session.close()
    
def query(comment_id):
    session = database.get_session()
    subcomments = session.query(SubComment).filter(SubComment.CommentId == comment_id).order_by(SubComment.CreateDate)
    session.close()
    return subcomments