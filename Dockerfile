FROM python:latest
RUN apt-get update && apt-get install -y postgresql postgresql-contrib
RUN pip install -r requirements.txt
CMD bash start.sh
