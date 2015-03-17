from flask import Flask
from projectTeam.controllers import *

def create_projectTeam_app():
    app = Flask(__name__)
    app.config.from_pyfile('powerteamconfig.py')
    app.jinja_env.variable_start_string = '(('
    app.jinja_env.variable_end_string = '))'
    app.register_module(home)
    app.register_module(project)
    app.register_module(task)
    app.register_module(team)
    app.register_module(issue)
    app.register_module(upload)
    app.register_module(user)
    app.register_module(admin)
    app.register_module(views)
    app.register_module(requirement)
    app.register_module(item)
    return app