import os
os.system('kill -9 $(sudo lsof -t -i:5000); gunicorn -b 0.0.0.0:5000 -k flask_sockets.worker module:app')
