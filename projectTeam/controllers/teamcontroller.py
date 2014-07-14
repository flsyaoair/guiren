# -*- coding: UTF-8 -*- 

from flask import Module,render_template, request, jsonify,g
from projectTeam.controllers.filters import login_filter
from projectTeam.services import teamservice, projectservice

team = Module(__name__)
team.before_request(login_filter)

@team.route('/Project/Team/<int:project_id>')
def list(project_id):
    p = projectservice.get(project_id)
    return render_template('Team/List.html',ProjectId=project_id,Creator =p.Creator,CurrentUser=g.user_id)

@team.route('/Team/GetMemberCandidate',methods=['POST'])
def member_candidate():
    project_id = request.json['ProjectId']
    member_list = teamservice.member_candidate(project_id)
    result = []
    for m in member_list:
        result.append({'Email':m.Email,'Nick':m.Nick})
    return jsonify(data=result)

@team.route('/Team/GetMemberInProject',methods=['POST'])
def member_in_project():
    project_id = request.json['ProjectId']
    member_list = teamservice.member_in_project(project_id)
    result = []
    for m in member_list:
        result.append({'Email':m.Email,'Nick':m.Nick,'UserId':m.UserId})
    return jsonify(data=result)

@team.route('/Team/AddMember',methods=['POST'])
def add_member():
    project_id = request.json['ProjectId']
    email = request.json['Email']
    teamservice.add_member(project_id,email)
    return jsonify(created=True)

@team.route('/Team/RemoveMember',methods=['POST'])
def remove_member():
    project_id = request.json['ProjectId']
    user_id = request.json['UserId']
    teamservice.remove_member(project_id,user_id)
    return jsonify(removed=True)