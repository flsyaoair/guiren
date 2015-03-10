# -*- coding: UTF-8 -*- 
from flask import Module,render_template,request,jsonify,g
from projectTeam.controllers.filters import login_filter
from projectTeam.services import requirementservice
from projectTeam.models import Project

requirement = Module(__name__)
requirement.before_request(login_filter)

@requirement.route('/Requirement')
def index():
    return render_template('Requirement/List.html')

@requirement.route('/Requirement/Create')
def create_requirement():
#    requirementservice.create(request.json['RequirementName'],request.json['Versions'],request.json['Description'],g.user_id)
    return render_template('Requirement/Create.html')
@requirement.route('/CreateRequirement',methods=['POST'])
def createNew_requirement():
    requirementservice.create(request.json['RequirementName'],request.json['Versions'],request.json['Description'],g.user_id)
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
#        d=i.Description.lstrip("<p>").rstrip("</p>")
        Requirement_list.append({'RequirementId':i.RequirementId,'RequirementName':i.RequirementName,'Description':i.Description,'Versions':i.Versions,'Status':i.Status,'LastUpdateDate':i.LastUpdateDate.isoformat()})
       
    return jsonify(data=Requirement_list)

@requirement.route('/Requirement/Detail/<int:requirement_id>')
def detail_requirement(requirement_id):
    requirementdetail = requirementservice.get(requirement_id)
    return render_template('Requirement/Detail.html',Requirementdetail=requirementdetail,RequirementId=requirement_id,Creator=requirementdetail.CreatorProfile.Nick,CurrentUser=g.user_id)                                             
@requirement.route('/Requirement/Update',methods=['POST'])
def update():
    requirement_id = request.json['RequirementId']
    requirement_name = request.json['RequirementName']
    version =  request.json['Versions']
    Description = request.json['Description']
    status = request.json['Status']
    requirementservice.update(requirement_id, requirement_name, version, status, Description, g.user_id)                
    return jsonify(updated=True)

#@requirement.route('/Requirement/Delete',methods=['POST'])
#def delete():
#    requirementservice.remove_RepositoryCategory(request.json['RequirementId'])
#    return jsonify(deleted=True)
if __name__ == '__main__':  
    requirement.run(host="0.0.0.0",port=8080, debug=True) 
