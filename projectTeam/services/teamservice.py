# -*- coding: UTF-8 -*- 

from projectTeam.models import UserProfile,database
from projectTeam.models.userprofile import UserStatus
from sqlalchemy.sql.elements import not_
from projectTeam.models.member import Member
from projectTeam.services import userservice, projectservice, mailservice
from projectTeam.powerteamconfig import *

def member_candidate(project_id):
    session = database.get_session()

    projectMember = session.query(Member.UserId).filter(Member.ProjectId == project_id)
    candidate = session.query(UserProfile).filter(UserProfile.Status == UserStatus.Enabled,not_(UserProfile.UserId.in_(projectMember)))

    session.close()
    return candidate

def member_in_project(project_id):
    session = database.get_session()

    projectMember = session.query(Member.UserId).filter(Member.ProjectId == project_id)
    memberList = session.query(UserProfile).filter(UserProfile.Status == UserStatus.Enabled,UserProfile.UserId.in_(projectMember))

    session.close()
    return memberList

def add_member(project_id,email):
    session = database.get_session()

    user = userservice.get(email)

    member = Member()
    member.ProjectId = project_id
    member.UserId = user.UserId

    session.add(member)
    session.commit()
    session.close()

    if ENABLE_MAIL_NOTICE:
        p = projectservice.get(project_id)
        body = mailservice.render_mail_template('Team/AddMember.html',ProjectName=p.ProjectName,SystemUrl=HOST)
        mailservice.send_mail(email,p.ProjectName + u'项目组欢迎您的加入:)',body)

def remove_member(project_id,user_id):
    session = database.get_session()

    session.query(Member).filter(Member.ProjectId == project_id,Member.UserId == user_id).delete()

    session.commit()
    session.close()

    if ENABLE_MAIL_NOTICE:
        p = projectservice.get(project_id)
        u = userservice.get_user_by_id(user_id)
        body = mailservice.render_mail_template('Team/RemoveMember.html',ProjectName=p.ProjectName,SystemUrl=HOST)
        mailservice.send_mail(u.Email, u'您已经被' + p.ProjectName + u'项目组移除',body)