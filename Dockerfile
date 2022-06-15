FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /home/workspace/link

WORKDIR /home/workspace/link

ADD . /home/workspace/link

RUN pip install -r requirements.txt

EXPOSE 8000 9000

# CMD chmod +x ./start.sh