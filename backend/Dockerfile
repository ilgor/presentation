FROM python:3.8
# RUN apt-get install sqlite
WORKDIR /backend
COPY ./requirements.txt /backend/
RUN pip install -r requirements.txt
RUN python3 -m ensurepip --upgrade
COPY . /backend/
# RUN sqlite3  -separator "," -cmd ".import users.csv users" database.db ".exit"
# CMD ["gunicorn", "--proxy-allow-from", "*", "--bind", "0.0.0.0:5000" ,"--log-level", "DEBUG", "-k", "geventwebsocket.gunicorn.workers.GeventWebSocketWorker", "-w", "1", "wsgi:app"]
CMD ["gunicorn", "--proxy-allow-from", "*", "--bind", "0.0.0.0:5000" ,"--log-level", "DEBUG", "-k", "eventlet", "-w", "1", "wsgi:app"]
