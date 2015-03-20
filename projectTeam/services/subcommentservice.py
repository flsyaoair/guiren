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
    
def query(comment_id,order_by,page_no,page_size):
    session = database.get_session()
    subcomments = session.query(SubComment).filter(SubComment.CommentId == comment_id)
    (row_count,page_count,page_no,page_size,subcomments) = database.pager_more(subcomments,order_by,page_no,page_size)
    subcomments_list = []
    for comment in subcomments.all():
        if comment.ReplyTo == -1:
            ReplyToNick = ''
        else:
            ReplyToNick = comment.ReplyToProfile.Nick
        subcomments_list.append({'SubCommentId':comment.SubCommentId, 'Content':comment.Content, 'CommentId':comment.CommentId, 'Creator':comment.Creator, 'CreatorNick':comment.CreatorProfile.Nick, 'ReplyTo':comment.ReplyTo, 'ReplyToNick':ReplyToNick, 'CreateDate':comment.CreateDate.isoformat()})

    session.close()
    return (subcomments_list,row_count,page_count,page_no)