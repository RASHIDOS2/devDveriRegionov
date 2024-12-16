FROM python:3.12


ENV PYTHONUBUFFERED=1


RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install psycopg2

WORKDIR /app

COPY ./requirements.txt ./

RUN pip install -r requirements.txt
COPY . .