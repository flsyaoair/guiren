# -*- coding: utf-8 -*-
from flask import Module,render_template,jsonify,redirect,request,g,session
from projectTeam.services import projectservice, taskservice, issueservice, teamservice, userservice, noticeservice
from projectTeam.controllers.filters import login_filter

notice = Module(__name__)
notice.before_request(login_filter)

@notice.route('/Notice/Create',methods=['POST'])
def create_notice():
    noticeservice.create(request.json['Content'])
    return jsonify(created=True)