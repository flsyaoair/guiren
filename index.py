# -*- coding: UTF-8 -*- 

from projectTeam import  create_projectTeam_app
from projectTeam.powerteamconfig import *

app = create_projectTeam_app()

if __name__ == '__main__':
    app.debug = True
    app.run(host= HOST,port=PORT)


#    app = create_projectTeam_app(config="config.yaml")

#    if app.debug: use_debugger = False 
#    try:
#        # Disable Flask's debugger if external debugger is requested
#        use_debugger = not(app.config.get(True))
#    except:
#        pass
#app.debug = False    app.run(use_debugger=use_debugger, debug=app.debug,
#            use_reloader=use_debugger, host= HOST,port=PORT)



#BAE
#from bae.core.wsgi import WSGIApplication
#application = WSGIApplication(app)

#handlers:
#  - url : /.*
#    script : index.py
#  - url : /static/(.*)
#    script : /powerteam/static/$1

#SAE
#import sae
#application = sae.create_wsgi_app(app)

#handlers:
#- url: /static
#  static_dir: powerteam/static