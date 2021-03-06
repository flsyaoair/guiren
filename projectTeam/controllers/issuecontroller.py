# -*- coding: UTF-8 -*- 

from flask import Module,render_template,request,g,jsonify
from projectTeam.controllers.filters import login_filter
from projectTeam.services import teamservice, issueservice,commentservice,subcommentservice,repositoryservice
from projectTeam.powerteamconfig import *

issue = Module(__name__)
issue.before_request(login_filter)

@issue.route('/Project/Issue/<int:project_id>')
def list(project_id):
    member_list = teamservice.member_in_project(project_id)
    category = issueservice.available_category()
    return render_template('Issue/List.html',ProjectId=project_id,MemberList=member_list,Category=category)

@issue.route('/Issue/Create/<int:project_id>')
def create(project_id):
    member_list = teamservice.member_in_project(project_id)
    projectmodules = repositoryservice.query_repositoryprofile(project_id)
    category = issueservice.available_category()
    return render_template('Issue/Create.html',ProjectId=project_id,MemberList=member_list,Category=category,ProjectModules=projectmodules)

@issue.route('/Issue/CreateNew',methods=['POST'])
def create_new():
    issueservice.create(request.json['ProjectId'],request.json['Subject'],request.json['ProjectModuleId'],request.json['Priority'],request.json['AssignTo'],request.json['Description'],request.json['CategoryId'],g.user_id)
    return jsonify(created=True,ProjectId=request.json['ProjectId'])

@issue.route('/Issue/Query',methods=['POST'])
def query():
    subject = request.json['Subject']
    assign_to = int(request.json['AssignTo'])
    if assign_to == -1:
        assign_to = g.user_id
    category_id = int(request.json['CategoryId'])
    status_open = request.json['Open']
    status_fixed = request.json['Fixed']
    status_closed = request.json['Closed']
    status_canceled = request.json['Canceled']
    page_no = request.json['PageNo']
    (row_count,page_count,page_no,page_size,data) = issueservice.query(subject,assign_to,category_id,status_open,status_fixed,status_closed,status_canceled,'CreateDate',page_no,PAGESIZE_issue,g.user_id)
    issue_list = []
    for i in data.all():
        issue_list.append({'IssueId':i.IssueId,'ProjectId':i.ProjectId,'ProjectKey':i.ProjectProfile.ProjectKey,'Category':i.Category.CategoryName,'Subject':i.Subject,'Priority':i.Priority,'Status':i.Status,'AssignTo':i.AssignToProfile.Nick,'Creator':i.CreatorProfile.Nick,'LastUpdateDate':i.LastUpdateDate.isoformat()})
    return jsonify(row_count=row_count,page_count=page_count,page_no=page_no,page_size=page_size,data=issue_list)

@issue.route('/Issue/Detail/<int:issue_id>')
def detail(issue_id):
    issue = issueservice.get(issue_id)
    projectmodules = repositoryservice.query_repositoryprofile(issue.ProjectId)
    modulerelation=repositoryservice.read_PlatformConfig(issue.ProjectId,issue.ProjectModuleId)
    member_list = teamservice.member_in_project(issue.ProjectId)
    category = issueservice.available_category()
    if issue.AssignTo == g.user_id:
        issue.AssignTo = -1
    history_list = issueservice.get_history(issue_id)
    return render_template('Issue/Detail.html',Issue=issue,HistoryList=history_list,Creator=issue.CreatorProfile.Nick,ProjectKey=issue.ProjectProfile.ProjectKey,MemberList=member_list,Category=category,CurrentUser=g.user_id,ModuleRelation=modulerelation)

@issue.route('/Issue/Update',methods=['POST'])
def update():
    ProjectId = request.json['ProjectId']
    IssueId = request.json['IssueId']
    subject = request.json['Subject']
    projectmodule_id = request.json['ProjectModuleId']
    assign_to = request.json['AssignTo']
    if int(assign_to) == -1:
        assign_to = g.user_id
    priority = request.json['Priority']
    category_id = request.json['CategoryId']
    status = request.json['Status']
    feedback = request.json['Feedback']
    issueservice.update(ProjectId,IssueId,subject,projectmodule_id,category_id,assign_to,priority,status,feedback,g.user_id)
    return jsonify(updated=True)

@issue.route('/Issue/Delete',methods=['POST'])
def delete():
    issueservice.delete(request.json['IssueId'])
    return jsonify(deleted=True)