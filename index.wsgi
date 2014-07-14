

﻿from powerteam import  create_powerteam_app
from powerteam.powerteamconfig import *

app = create_powerteam_app()

#if __name__ == '__main__':
#    app.run(host= HOST,port=PORT)

#BAE
#from bae.core.wsgi import WSGIApplication
#application = WSGIApplication(app)

#handlers:
#  - url : /.*
#    script : index.py
#  - url : /static/(.*)
#    script : /powerteam/static/$1

#SAE
import sae
application = sae.create_wsgi_app(app)

#handlers:
#- url: /static
#  static_dir: powerteam/static