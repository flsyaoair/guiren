# -*- coding: UTF-8 -*- 
#from flask import Flask
#app = Flask(__name__)
from projectTeam.controllers.homecontroller import home
from projectTeam.controllers.projectcontroller import project
from projectTeam.controllers.taskcontroller import task
from projectTeam.controllers.teamcontroller import team
from projectTeam.controllers.issuecontroller import issue
from projectTeam.controllers.uploadcontroller import upload
from projectTeam.controllers.usercontroller import user
from projectTeam.controllers.admincontroller import admin
from projectTeam.controllers.views import views
from projectTeam.controllers.noticecontroller import notice
from projectTeam.controllers.requirementcontroller import requirement

