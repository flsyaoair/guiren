# -*- coding: utf-8 -*-
from projectTeam.models import Notice, database
from datetime import datetime

def get():
    session = database.get_session()
    n = session.query(Notice).order_by(Notice.CreateDate.desc()).first()
    session.close()
    return n
    
def create(content):
    session = database.get_session()
    n = Notice()
    n.Content = content.strip()
    n.CreateDate = datetime.now()
    session.add(n)
    session.commit()
    session.close()
    