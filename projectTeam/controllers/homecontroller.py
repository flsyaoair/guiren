# -*- coding: UTF-8 -*- 

from datetime import *

from flask import Module,render_template,jsonify, redirect, request,session
from projectTeam.models import database
from projectTeam.services import userservice, mailservice
from projectTeam.models.userprofile import UserStatus

home = Module(__name__)

@home.route('/')
def index():
    if 'username' in session and not session['username'] == None:
        return redirect('/Project')
    return render_template('Login.html')

@home.route('/Login',methods=['POST'])
def login():
    email = request.json['Email']
    password = request.json['Password']
    user = userservice.get(request.json['Email'])
    if user == None:
        response = jsonify(isDisabled = False,isMatch=False)
        return response

    if user.Status == UserStatus.Disabled:
        response = jsonify(isDisabled = True,isMatch=None)
        return response

    if not user.Password == password:
        response = jsonify(isDisabled = False,isMatch=False)
        return response

    session['userid'] = user.UserId
    session['username'] = user.Email
    session['isadmin'] = user.IsAdmin
    response = jsonify(isDisabled=False,isMatch=True)
    return response

@home.route('/Register')
def register():
    return render_template('Register.html')

@home.route('/Register/Save',methods=['POST'])
def save():
    (exist,userid) = userservice.register(request.json['Email'],request.json['Nick'],request.json['Password'])

    if not exist:
        session['userid'] = userid
        session['username'] = request.json['Email']
    session['isadmin'] = False
    result = {'created' : not exist}
    return jsonify(result)


#@home.route('/Install')
#def install():
#    import sys
#    from powerteam.models import database, UserProfile,UserStatus, IssueCategory, IssueCategoryStatus
#    from datetime import datetime

#    database.drop_database()

#    database.create_database()

#    session = database.get_session()
#    admin = UserProfile()
#    admin.Email = 'admin@admin.com'
#    admin.Nick = u'admin'
#    admin.Password = 'admin'
#    admin.Status = UserStatus.Enabled
#    admin.IsAdmin = True
#    admin.RegDate = datetime.now()
#    session.add(admin)

#    bug = IssueCategory()
#    bug.CategoryName = u'Bug'
#    bug.Status = IssueCategoryStatus.Enabled

#    issue = IssueCategory()
#    issue.CategoryName = u'Issue'
#    issue.Status = IssueCategoryStatus.Enabled

#    session.add(bug)
#    session.add(issue)

#    session.commit()
#    session.close()
