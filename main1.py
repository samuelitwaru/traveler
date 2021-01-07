import os
os.system('kill -9 $(sudo lsof -t -i:8000); gunicorn -k flask_sockets.worker module:app')
