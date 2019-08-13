FROM ubuntu:latest

ENV https_proxy http://192.168.2.1:3128
ENV http_proxy http://192.168.2.1:3128

RUN apt-get update -y

RUN apt-get install -y python-pip python-dev build-essential

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
