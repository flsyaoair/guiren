# -*- coding: utf-8 -*-
from flask import Module,render_template,request,jsonify,g
from projectTeam.controllers.filters import login_filter
from projectTeam.services import commentservice,subcommentservice
from projectTeam.powerteamconfig import *

comment = Module(__name__)
comment.before_request(login_filter)

@comment.route('/Comment/Create',methods=['POST'])
def create_comment():
    content = request.json['Content']
    task_id = request.json['TaskId']
    issue_id = request.json['IssueId']
    requirement_id = request.json['RequirementId']
    creator = g.user_id
    comment_id = commentservice.create(content, task_id, issue_id, requirement_id, creator)
    return jsonify(created=True,comment_id=comment_id)
    
@comment.route('/Comment/Query',methods=['POST'])
def query_comment():
    task_id = request.json['TaskId']
    issue_id = request.json['IssueId']
    requirement_id = request.json['RequirementId']
    page_no = request.json['PageNo']
    (comments,row_count,page_count,page_no) = commentservice.query(task_id, issue_id, requirement_id,'CreateDate',page_no,PAGESIZE_comment)
    return jsonify(data=comments,row_count=row_count,page_count=page_count,page_no=page_no)
    
@comment.route('/SubComment/Create',methods=['POST'])
def create_subcomment():
    content = request.json['Content']
    comment_id = request.json['CommentId']
    replyto = request.json['ReplyTo']
    creator = g.user_id
    subcommentservice.create(content, comment_id, replyto, creator)
    return jsonify(created=True)
    
@comment.route('/SubComment/Reply',methods=['POST'])
def reply_subcomment():
    content = request.json['ReplyContent']
    comment_id = request.json['CommentId']
    replyto = request.json['ReplyTo']
    creator = g.user_id
    subcommentservice.create(content, comment_id, replyto, creator)
    return jsonify(created=True)
    
@comment.route('/SubComment/Query',methods=['POST'])
def query_subcomment():
    comment_id = request.json['CommentId']
    page_no = request.json['PageNo']
    (subcomments,row_count,page_count,page_no) = subcommentservice.query(comment_id,'CreateDate',page_no,PAGESIZE_subcomment)
    return jsonify(data=subcomments,row_count=row_count,page_count=page_count,page_no=page_no)