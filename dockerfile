FROM python:3.12

ADD app/ /app

RUN pip install -r requirements.txt

RUN chmod +X setup.sh