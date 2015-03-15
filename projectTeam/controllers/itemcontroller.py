# -*- coding: UTF-8 -*- 
from flask import Module,render_template,request,jsonify,g
from projectTeam.controllers.filters import login_filter
from projectTeam.services import requirementservice
from projectTeam.models import Project

item = Module(__name__)
item.before_request(login_filter)

@item.route('/Item')
def index():
    return render_template('Item/List.html')
# 
# @item.route('/Item/Create')
# def create_requirement():
# #    requirementservice.create(request.json['RequirementName'],request.json['Versions'],request.json['Description'],g.user_id)
#     return render_template('Item/Create.html')
# @item.route('/CreateItem',methods=['POST'])
# def createNew_item():
#     itemservice.create(request.json['ItemName'])
#     return jsonify(created=True)
#def list(project_id):
#
#    return render_template('Requirement/List.html',ProjectId=project_id,MemberList=member_list,ProjectNameList=project_name)
#
# @item.route('/Item/Query',methods=['POST'])
# def query():
# #    requirement_id = request.json['RequirementId']
# #     status = request.json['Status']
#     page_no = request.json['PageNo']
#     (row_count,page_count,page_no,page_size,data) = requirementservice.query(status,page_no,'LastUpdateDate desc')
#     Requirement_list=[]
#     for i in data:
# #        d=i.Description.lstrip("<p>").rstrip("</p>")
#         Requirement_list.append({'RequirementId':i.RequirementId,'RequirementName':i.RequirementName,'Description':i.Description,'Versions':i.Versions,'Status':i.Status,'LastUpdateDate':i.LastUpdateDate.isoformat()})
#        
#     return jsonify(row_count=row_count,page_count=page_count,page_no=page_no,page_size=page_size,data=Requirement_list)

# @requirement.route('/Requirement/Update',methods=['POST'])
# def update():
#     requirement_id = request.json['RequirementId']
#     requirement_name = request.json['RequirementName']
#     version =  request.json['Versions']
#     Description = request.json['Description']
#     status = request.json['Status']
#     requirementservice.update(requirement_id, requirement_name, version, status, Description, g.user_id)                
#     return jsonify(updated=True)


if __name__ == '__main__':  
    item.run(host="0.0.0.0",port=8080, debug=True) 
