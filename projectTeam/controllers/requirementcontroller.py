# -*- coding: UTF-8 -*- 
from flask import Module,render_template,request,jsonify,g
from projectTeam.controllers.filters import login_filter
from projectTeam.services import requirementservice
from projectTeam.models import Project

requirement = Module(__name__)
requirement.before_request(login_filter)

@requirement.route('/Requirement')
def index():
#    requirementservice.create(request.json['RequirementName'],request.json['Versions'],request.json['Status'],request.json['Description'],g.user_id)
    return render_template('Requirement/List.html')

@requirement.route('/Requirement/Create')

def create_requirement():
#    requirementservice.create(request.json['RequirementName'],request.json['Versions'],request.json['Description'],g.user_id)
    return render_template('Requirement/Create.html')
@requirement.route('/CreateRequirement',methods=['POST'])
def createNew_requirement():
    requirementservice.create(request.json['RequirementName'],request.json['Versions'],request.json['Description'])
    return jsonify(created=True)
#def list(project_id):
#
#    return render_template('Requirement/List.html',ProjectId=project_id,MemberList=member_list,ProjectNameList=project_name)
#
@requirement.route('/Requirement/Query',methods=['POST'])
def query():
#    requirement_id = request.json['RequirementId']
    data = requirementservice.query()
    Requirement_list=[]
    for i in data:
        Requirement_list.append({'RequirementId':i.RequirementId,'RequirementName':i.RequirementName})
#  
    return jsonify(data=Requirement_list)

                                              
#@task.route('/Task/Update',methods=['POST'])
#def update():
#    task_id = request.json['TaskId']
#    project_id = request.json['ProjectId']
#    task_name = request.json['TaskName']
#    version =  request.json['Versions']
#    feedback = request.json['Feedback']
#    assign_to = request.json['AssignTo']
#    if assign_to == -1:
#        assign_to = g.user_id
#    priority = request.json['Priority']
#    progress = request.json['Progress']
#    status = request.json['Status']
##    effort = request.json['Effort']
##    description = request.json['Description']
#    taskservice.update(task_id, task_name, version, assign_to, priority, progress, status, feedback, g.user_id)                
#    return jsonify(updated=True)

#@requirement.route('/Requirement/Delete',methods=['POST'])
#def delete():
#    requirementservice.remove_RepositoryCategory(request.json['RequirementId'])
#    return jsonify(deleted=True)
if __name__ == '__main__':  
    requirement.run(host="0.0.0.0",port=8080, debug=True) 
