# -*- coding: UTF-8 -*- 

from flask import Module,request,jsonify
from projectTeam.controllers.filters import login_filter
import os
from projectTeam.powerteamconfig import *
import uuid

upload = Module(__name__)
upload.before_request(login_filter)

@upload.route('/uploadimg',methods=['POST'])
def uploadimg():
    file = request.files['upfile']
    ext = file.filename.split('.')[-1]
    filename = str(uuid.uuid4()) + '.' + ext
    if not os.path.exists(UPLOADPATH):
        os.makedirs(UPLOADPATH)
    file.save(os.path.join(UPLOADPATH, filename))
    return jsonify(url=os.path.join(UPLOADDIR, filename))