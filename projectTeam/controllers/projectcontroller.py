# -*- coding: UTF-8 -*- 

from flask import Module,render_template,jsonify,redirect,request,g,session
from projectTeam.services import projectservice, taskservice, issueservice, teamservice,userservice
from projectTeam.controllers.filters import login_filter

project = Module(__name__)
project.before_request(login_filter)

@project.route('/Project')
def index():
    #history_list = taskservice.get_user_history(g.user_id)
    task_list = taskservice.member_task(g.user_id)
    history_list_all = []
    for task in task_list:
        history_list = taskservice.get_history(task.TaskId)
        for history in history_list:
            history_list_all.append(history)

    return render_template('Project/List.html', TaskList=task_list, HistoryList=history_list_all)

@project.route('/Project/Query',methods=['POST'])
def query():
    project_name = request.json['ProjectName']
    project_introduction = request.json['Introduction']
    status = request.json['Status']
    page_no = request.json['PageNo']
    (row_count,page_count,page_no,page_size,data) = projectservice.query(project_name,project_introduction,status,page_no,'CreateDate desc',g.user_id)
    projects = []
    for p in data.all():
        projects.append({'ProjectId':p.ProjectId,'ProjectName':p.ProjectName,'Introduction':p.Introduction,'Status':p.Status,'Progress':p.Progress,'CreateDate':p.CreateDate.isoformat(),'Creator':p.UserProfile.Nick,'ProjectKey':p.ProjectKey})
    return jsonify(row_count=row_count,page_count=page_count,page_no=page_no,page_size=page_size,data=projects)

@project.route('/Project/Create',methods=['POST'])
def create():
    projectservice.create(request.json['ProjectName'],request.json['ProjectKey'],request.json['Introduction'],g.user_id)
    return jsonify(created=True)

@project.route('/Project/Delete',methods=['POST'])
def delete():
    projectservice.delete(request.json['ProjectId'])
    return jsonify(deleted=True)

@project.route('/Project/Detail/<int:project_id>')
def detail(project_id):
    project = projectservice.get(project_id)

    return render_template('Project/Detail.html',Project=project,ProjectKey=project.ProjectKey,CreatorName=project.UserProfile.Nick,CurrentUser=g.user_id)

@project.route('/Project/Update',methods=['POST'])
def update():
    project_id = request.json['ProjectId']
    project_name = request.json['ProjectName']
    project_introduction = request.json['Introduction']
    status = request.json['Status']
    projectservice.update(project_id,project_name,project_introduction,status)
    return jsonify(updated=True)

@project.route('/Project/Dashboard/<int:project_id>')
def dashboard(project_id):
    (task_status,task_priority) = taskservice.statistics(project_id)
    (issue_status,issue_priority) = issueservice.statistics(project_id)
    project = projectservice.get(project_id)
    member_list = teamservice.member_in_project(project_id)
    return render_template('Project/Dashboard.html',Project=project,TaskStatus=task_status,TaskPriority=task_priority,IssueStatus=issue_status,IssuePriority=issue_priority,MemberList=member_list)