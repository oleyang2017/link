FROM python:3.10

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /home/workspace/link

WORKDIR /home/workspace/link

ADD . /home/workspace/link

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 8000 9000

CMD ["supervisord", "-c", "./supervisord.conf"]
