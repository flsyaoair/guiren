# -*- coding: UTF-8 -*- 
from flask import Module,render_template,request,jsonify
from projectTeam.controllers.filters import admin_filter
from projectTeam.services import userservice,issueservice,repositoryservice

admin = Module(__name__)
admin.before_request(admin_filter)

@admin.route('/Admin')
def index():
    return render_template('Admin/index.html')

@admin.route('/Admin/CategorySetting')
def category():
    return render_template('Admin/CategorySetting.html')

@admin.route('/Admin/RepositorySetting')
def repository():
    return render_template('Admin/RepositorySetting.html')

@admin.route('/QueryUser',methods=['POST'])
def query():
    mail_or_nick = request.json['Word']
    status = request.json['Status']
    page_no = request.json['PageNo']

    (row_count,page_count,page_no,page_size,data) = userservice.query_user(mail_or_nick,int(status),"RegDate desc",page_no)
    user_list = []
    for i in data.all():
        user_list.append({'UserId':i.UserId,'Email':i.Email,'Nick':i.Nick,'Status':i.Status,'IsAdmin':i.IsAdmin,'RegDate':i.RegDate.isoformat()})
    return jsonify(row_count=row_count,page_count=page_count,page_no=page_no,page_size=page_size,data=user_list)

@admin.route('/EnableUser',methods=['POST'])
def enable_user():
    userid = request.json['UserId']
    userservice.enable_user(userid)
    return jsonify(status='ok')

@admin.route('/DisableUser',methods=['POST'])
def disable_user():
    userid = request.json['UserId']
    userservice.disable_user(userid)
    return jsonify(status='ok')

@admin.route('/ResetPassword',methods=['POST'])
def reset_password():
    userid = request.json['UserId']
    userservice.reset_password(userid)
    return jsonify(status='ok')

@admin.route('/AssignAdmin',methods=['POST'])
def assign_admin():
    userid = request.json['UserId']
    userservice.assign_admin(userid)
    return jsonify(status='ok')

@admin.route('/QueryCategory',methods=['POST'])
def query_category():
    data = issueservice.all_category()
    category_list = []
    for i in data:
        category_list.append({'CategoryId':i.CategoryId,'CategoryName':i.CategoryName,'Status':i.Status})
    return jsonify(data=category_list)

@admin.route('/EnableCategory',methods=['POST'])
def enable_category():
    categoryid = request.json['CategoryId']
    issueservice.enable_category(categoryid)
    return jsonify(status='ok')

@admin.route('/DisableCategory',methods=['POST'])
def disable_category():
    categoryid = request.json['CategoryId']
    issueservice.disable_category(categoryid)
    return jsonify(status='ok')

@admin.route('/CreateCategory',methods=['POST'])
def create_category():
    categoryname = request.json['CategoryName']
    exist = issueservice.exist_category(categoryname)
    if not exist:
        issueservice.create_category(categoryname)
    return jsonify(status=exist)
@admin.route('/CreateRepository',methods=['POST'])
def create_Repository():
    repositoryname = request.json['RepositoryName']
    exist = repositoryservice.exist_repository(repositoryname)
    if not exist:
        repositoryservice.create_repository(repositoryname)
    return jsonify(status=exist)
@admin.route('/QueryRepository',methods=['POST'])
def query_Repository():
    
    data = repositoryservice.query_repository()
    repository_list = []
    for i in data:
        repository_list.append({'RepositoryId':i.RepositoryId,'RepositoryName':i.RepositoryName})
    return jsonify(data=repository_list)
@admin.route('/Repository/Detail/<int:repository_id>')
def detail_Repository(repository_id):   
    repository = repositoryservice.get(repository_id)
#    tt=repository.RepositoryName
    return render_template('Repository/Detail.html',RepositoryId=repository_id,Repository=repository) 
@admin.route('/RemoveRepository',methods=['POST'])
def remove_Repository():
    repository_id = request.json['RepositoryId']
#    repositoryCategory_id = request.json['RepositoryCategoryId']
    repositoryservice.remove_Repository(repository_id)
    return jsonify(removed=True)   

@admin.route('/CreateRepositoryCategory',methods=['POST'])
def create_RepositoryCategory():
    repositorycategoryname = request.json['RepositoryCategoryName']
    repositoryid = request.json['RepositoryId']
#    repository = repositoryservice.get(repository_id)
#    repositoryid=repository.RepositoryId
    exist = repositoryservice.exist_repositoryprofile(repositoryid,repositorycategoryname)
    if not exist:
        repositoryservice.create_repositoryprofile(repositoryid,repositorycategoryname)
    return jsonify(status=exist,RepositoryId=repositoryid)  
@admin.route('/QueryRepositoryCategory',methods=['POST'])
def query_RepositoryCategory():
    
    repository_id = request.json['RepositoryId']
    data = repositoryservice.query_repositoryprofile(repository_id)
    repositoryCategory_list = []
    for i in data:
        repositoryCategory_list.append({'RepositoryCategoryId':i.RepositoryCategoryId,'RepositoryCategoryName':i.RepositoryCategoryName})
    return jsonify(data=repositoryCategory_list) 
@admin.route('/RemoveRepositoryCategory',methods=['POST'])
def remove_RepositoryCategory():
    repository_id = request.json['RepositoryId']
    repositoryCategory_id = request.json['RepositoryCategoryId']
    repositoryservice.remove_RepositoryCategory(repository_id,repositoryCategory_id)
    return jsonify(removed=True)   