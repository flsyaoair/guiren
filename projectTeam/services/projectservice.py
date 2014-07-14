# -*- coding: UTF-8 -*- 

from projectTeam.models import Project, ProjectStatus,database, Member, Task
from datetime import datetime
from sqlalchemy.orm import joinedload

def create(project_name,creator):
    session = database.get_session()

    p = Project()
    p.ProjectName = project_name.strip()
    p.Status = ProjectStatus.InProgress
    p.Progress = 0
    p.Creator = creator
    p.CreateDate = datetime.now()
    p.LastUpdateDate = datetime.now()

    m = Member()
    m.UserId = creator
    p.Members.append(m)

    session.add(p)
    session.commit()
    session.close()

def get(project_id):
    session = database.get_session()

    p = session.query(Project).options(joinedload(Project.UserProfile)).filter(Project.ProjectId == project_id).one()

    session.close()
    return p

def query(project_name,status,page_no,order_by,current_user):
    filters = []
    project_name = project_name.strip()
    if len(project_name) > 0:
        filters.append(Project.ProjectName.like('%' + project_name + '%'))
    if not status == '-1':
        filters.append(Project.Status == status)

    session = database.get_session()

    project_list = session.query(Member.ProjectId).filter(Member.UserId == current_user)

    q = session.query(Project).filter(Project.ProjectId.in_(project_list))
    for f in filters:
        q = q.filter(f)
    (row_count,page_count,page_no,page_size,data) = database.pager(q,order_by,page_no)

    session.close()
    return (row_count,page_count,page_no,page_size,data)

def delete(project_id):
    session = database.get_session()

    session.query(Member).filter(Member.ProjectId == project_id).delete()
    session.query(Task).filter(Task.ProjectId == project_id).delete()
    session.query(Project).filter(Project.ProjectId == project_id).delete()

    session.commit()
    session.close()

def update(project_id,project_name,status):
    session = database.get_session()

    session.query(Project).filter(Project.ProjectId == project_id).update({'ProjectName':project_name.strip(),'Status':status,'LastUpdateDate':datetime.now()})

    session.commit()
    session.close()

    return True