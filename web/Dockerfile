FROM python:2.7
#ENV https_proxy http://192.168.2.1:3128
#ENV http_proxy http://192.168.2.1:3128

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]