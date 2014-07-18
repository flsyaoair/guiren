# -*- coding: UTF-8 -*- 
from flask import Module,render_template,request,jsonify,g
from projectTeam.controllers.filters import login_filter
from projectTeam.services import teamservice,taskservice

task = Module(__name__)
task.before_request(login_filter)

@task.route('/Project/Task/<int:project_id>')
def list(project_id):
    member_list = teamservice.member_in_project(project_id)
    return render_template('Task/List.html',ProjectId=project_id,MemberList=member_list)

@task.route('/Task/Query',methods=['POST'])
def query():
    task_name = request.json['TaskName']
    assign_to = int(request.json['AssignTo'])
    if assign_to == -1:
        assign_to = g.user_id
    status_new = request.json['New']
    status_in_progress = request.json['InProgress']
    status_completed = request.json['Completed']
    status_canceled = request.json['Canceled']
    page_no = request.json['PageNo']
    (row_count,page_count,page_no,page_size,data) = taskservice.query(task_name,assign_to,status_new,status_in_progress,status_completed,status_canceled,'Priority',page_no)
    tasks = []
    for t in data.all():
        tasks.append({'TaskId':t.TaskId,'TaskName':t.TaskName,'Priority':t.Priority,'Progress':t.Progress,'Status':t.Status,'Effort':t.Effort,'AssignTo':t.AssignToProfile.Nick,'Creator':t.CreatorProfile.Nick,'LastUpdateDate':t.LastUpdateDate.isoformat()})
    return jsonify(row_count=row_count,page_count=page_count,page_no=page_no,page_size=page_size,data=tasks)

@task.route('/Task/Create/<int:project_id>')
def create(project_id):
    member_list = teamservice.member_in_project(project_id)
    return render_template('Task/Create.html',ProjectId=project_id,MemberList=member_list)

@task.route('/Task/Detail/<int:task_id>')
def detail(task_id):
    t = taskservice.get(task_id)
    member_list = teamservice.member_in_project(t.ProjectId)
    if t.AssignTo == g.user_id:
        t.AssignTo = -1

    return render_template('Task/Detail.html',Task=t,Creator=t.CreatorProfile.Nick,MemberList=member_list,CurrentUser=g.user_id)

@task.route('/Task/Update',methods=['POST'])
def update():
    task_id = request.json['TaskId']
    project_id = request.json['ProjectId']
    task_name = request.json['TaskName']
    feedback = request.json['Feedback']
    assign_to = request.json['AssignTo']
    if assign_to == -1:
        assign_to = g.user_id
    priority = request.json['Priority']
    progress = request.json['Progress']
    status = request.json['Status']
    effort = request.json['Effort']
#    description = request.json['Description']
    taskservice.update(task_id,task_name,assign_to,priority,progress,status,effort,feedback)
    return jsonify(updated=True)

@task.route('/Task/Delete',methods=['POST'])
def delete():
    taskservice.delete(request.json['TaskId'])
    return jsonify(deleted=True)

@task.route('/Task/CreateNew',methods=['POST'])
def create_new():
    taskservice.create(request.json['ProjectId'],request.json['TaskName'],request.json['Priority'],request.json['AssignTo'],request.json['Description'],g.user_id)
    return jsonify(created=True,ProjectId=request.json['ProjectId'])