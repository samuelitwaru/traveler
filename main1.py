import os
os.system('sudo kill -9 $(sudo lsof -t -i:8000); gunicorn -k flask_sockets.worker module:app')
