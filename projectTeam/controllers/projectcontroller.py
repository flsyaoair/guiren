# -*- coding: UTF-8 -*- 

from flask import Module,render_template,jsonify,redirect,request,g,session,Markup
from projectTeam.services import projectservice, taskservice, issueservice, teamservice,userservice, noticeservice
from projectTeam.controllers.filters import login_filter
from operator import attrgetter, itemgetter

project = Module(__name__)
project.before_request(login_filter)

@project.route('/Project')
def index():
    task_list = taskservice.member_task(g.user_id)
    issue_list = issueservice.member_issue(g.user_id)
    history_list_all = []
    for task in task_list:
        history_list_task = taskservice.get_history(task.TaskId)
        for history in history_list_task:
            history_list_all.append(history)
    for issue in issue_list:
        history_list_issue = issueservice.get_history(issue.IssueId)
        for history in history_list_issue:
            history_list_all.append(history)
#    history_list_all = sorted(history_list_all, key=lambda history: history.CreateDate, reverse=True)  #第二种写法
    history_list_all = sorted(history_list_all, key=attrgetter('CreateDate'), reverse=True)
    length = len(history_list_all)
    notice_content = noticeservice.get()
#    Notice = request.json['Notice']
#    noticeservice.create(Notice)
    return render_template('Project/List.html', HistoryList=history_list_all, Length=length, Content=notice_content)

@project.route('/History',methods=['POST'])
def history():
    task_list = taskservice.member_task(g.user_id)
    issue_list = issueservice.member_issue(g.user_id)
    history_list_all = []
    for task in task_list:
        history_list_task = taskservice.get_history(task.TaskId)
        for history in history_list_task:
            history_list_all.append({'ProjectId':history.ProjectId, 'ProjectName':history.ProjectProfile.ProjectName,  'Name':history.Name, 'TaskId':history.TaskId, 'IssueId':'', 'CreateDate':history.CreateDate.strftime('%Y-%m-%d %H:%M'),'RawAssignTo':history.RawAssignToProfile.Nick, 'NewAssignTo':history.NewAssignToProfile.Nick, 'RawStatus':history.RawStatus, 'NewStatus':history.NewStatus, 'RawPriority':history.RawPriority, 'NewPriority':history.NewPriority, 'Feedback':history.Feedback})           
    for issue in issue_list:
        history_list_issue = issueservice.get_history(issue.IssueId)
        for history in history_list_issue:
            history_list_all.append({'ProjectId':history.ProjectId, 'ProjectName':history.ProjectProfile.ProjectName,  'Name':history.Name, 'TaskId':'', 'IssueId':history.IssueId, 'CreateDate':history.CreateDate.strftime('%Y-%m-%d %H:%M'),'RawAssignToProfile.Nick':history.RawAssignToProfile.Nick, 'NewAssignToProfile.Nick':history.NewAssignToProfile.Nick, 'RawStatus':history.RawStatus, 'NewStatus':history.NewStatus, 'RawPriority':history.RawPriority, 'NewPriority':history.NewPriority, 'Feedback':history.Feedback})
#    history_list_all = sorted(history_list_all, key=lambda history: history.CreateDate, reverse=True)  #第二种写法
    history_list_all = sorted(history_list_all, key=itemgetter('CreateDate'), reverse=True)
#    history_list_all = Markup(history_list_all)
    return jsonify(data=history_list_all)

@project.route('/Project/Query',methods=['POST'])
def query():
    project_name = request.json['ProjectName']
    project_introduction = request.json['Introduction']
    status = request.json['Status']
    page_no = request.json['PageNo']
    (row_count,page_count,page_no,page_size,data) = projectservice.query(project_name,project_introduction,status,page_no,'LastUpdateDate desc',g.user_id)
    projects = []
    for p in data.all():
        projects.append({'ProjectId':p.ProjectId,'ProjectName':p.ProjectName,'Introduction':p.Introduction,'Status':p.Status,'Progress':p.Progress,'CreateDate':p.CreateDate.isoformat(),'LastUpdateDate':p.LastUpdateDate.isoformat(),'Creator':p.UserProfile.Nick,'ProjectKey':p.ProjectKey})
    return jsonify(row_count=row_count,page_count=page_count,page_no=page_no,page_size=page_size,data=projects,data2=projects[:5])

@project.route('/Project/Create',methods=['POST'])
def create():
    try:
        Introduction = request.json['Introduction']
    except KeyError,e:
        Introduction = ''
    exist = projectservice.create(request.json['ProjectName'],request.json['ProjectKey'],Introduction,g.user_id)
    exist_json = {'exist': exist}
    print exist_json
    return jsonify(exist_json)

    
@project.route('/Notice/Create',methods=['POST'])
def create_notice():
    noticeservice.create(request.json['Content'])
    return jsonify(created=True)

@project.route('/Notice/Query',methods=['POST'])
def query_notice():
#    notice_content = request.json['Content']
    data = noticeservice.get()
    data_dic = {'Content':data.Content, 'Date':data.CreateDate.isoformat()}
    return jsonify(data=data_dic)
    
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