
from flask import Module
views = Module(__name__)

@views.route('/index')
@views.route('/index')
def index():
#    if i==1:
        
     return "Hello, World!!!!!!!!!"