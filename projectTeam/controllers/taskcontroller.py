# -*- coding: UTF-8 -*- 
from flask import Module,render_template,request,jsonify,g
from projectTeam.controllers.filters import login_filter
from projectTeam.services import teamservice,taskservice,projectservice
from projectTeam.models import Project

task = Module(__name__)
task.before_request(login_filter)

@task.route('/Project/Task/<int:project_id>')
def list(project_id):
    member_list = teamservice.member_in_project(project_id)
#    project_name= Project.ProjectName
    project_name = projectservice.projectlist()
    return render_template('Task/List.html',ProjectId=project_id,MemberList=member_list,ProjectNameList=project_name)

@task.route('/Task/Query',methods=['POST'])
def query():
    task_name = request.json['TaskName']
    project_id =request.json["ProjectId"]
#    project_name = request.json['ProjectName']
    assign_to = int(request.json['AssignTo'])
    if assign_to == -1:
        assign_to = g.user_id
    status_new = request.json['New']
    status_in_progress = request.json['InProgress']
    status_completed = request.json['Completed']
    status_canceled = request.json['Canceled']
    page_no = request.json['PageNo']
    (row_count,page_count,page_no,page_size,data) = taskservice.query(task_name,project_id,assign_to,status_new,status_in_progress,status_completed,status_canceled,'Priority',page_no,g.user_id)
    tasks = []
    for t in data.all():
        tasks.append({'TaskId':t.TaskId,'ProjectId':project_id,'ProjectKey':t.ProjectProfile.ProjectKey,'TaskName':t.TaskName,'Priority':t.Priority,'Progress':t.Progress,'Status':t.Status,'Effort':t.Effort,'AssignTo':t.AssignToProfile.Nick,'Creator':t.CreatorProfile.Nick,'LastUpdateDate':t.LastUpdateDate.isoformat()})
    return jsonify(row_count=row_count,page_count=page_count,page_no=page_no,page_size=page_size,data=tasks)

@task.route('/Task/Create/<int:project_id>')
def create(project_id):
    member_list = teamservice.member_in_project(project_id)
#    task = taskservice.get(member_list.TaskId)
    return render_template('Task/Create.html',ProjectId=project_id,MemberList=member_list)

@task.route('/Task/Detail/<int:task_id>')
def detail(task_id):
    task = taskservice.get(task_id)
    history_list = taskservice.get_history(task_id)
    member_list = teamservice.member_in_project(task.ProjectId)
    if task.AssignTo == g.user_id:
        task.AssignTo = -1
    
   
    return render_template('Task/Detail.html',Task=task,HistoryList=history_list,Creator=task.CreatorProfile.Nick,ProjectKey=task.ProjectProfile.ProjectKey,MemberList=member_list,CurrentUser=g.user_id)
                                              
@task.route('/Task/Update',methods=['POST'])
def update():
    task_id = request.json['TaskId']
    project_id = request.json['ProjectId']
    task_name = request.json['TaskName']
    version =  request.json['Versions']
    feedback = request.json['Feedback']
    assign_to = request.json['AssignTo']
    if assign_to == -1:
        assign_to = g.user_id
    priority = request.json['Priority']
    progress = request.json['Progress']
    status = request.json['Status']
#    effort = request.json['Effort']
#    description = request.json['Description']
    taskservice.update(project_id, task_id, task_name, version, assign_to, priority, progress, status, feedback, g.user_id)                
    return jsonify(updated=True)

@task.route('/Task/Delete',methods=['POST'])
def delete():
    taskservice.delete(request.json['TaskId'])
    return jsonify(deleted=True)

@task.route('/Task/CreateNew',methods=['POST'])
def create_new():
    taskservice.create(request.json['ProjectId'],request.json['TaskName'],request.json['Versions'],request.json['Priority'],request.json['AssignTo'],request.json['Description'],g.user_id)
    return jsonify(created=True,ProjectId=request.json['ProjectId'])