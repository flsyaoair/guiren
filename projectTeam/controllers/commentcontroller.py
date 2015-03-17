# -*- coding: utf-8 -*-
from flask import Module,render_template,request,jsonify,g
from projectTeam.controllers.filters import login_filter
from projectTeam.services import teamservice,taskservice,projectservice
from projectTeam.models import Task,Issue,Requirement
from projectTeam.services import commentservice, issueservice
from projectTeam.controllers.taskcontroller import *

comment = Module(__name__)
comment.before_request(login_filter)

@comment.route('/Comment/Create',methods=['POST'])
def create_comment():
    print '----------------------------------------------------------'
    print '-------------------comment---------------------------------------'
#    commentservice.create()
    return jsonify(created=True)