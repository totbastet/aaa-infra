FROM python:3.8
ENV FLASK_APP=server

LABEL version="0.1.0"

WORKDIR server
COPY . /server

RUN pip install -r requirements.txt

EXPOSE 8080
CMD flask run -h 0.0.0.0 -p 8080