FROM ubuntu:latest
RUN sed -i 's/archive.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN apt update && apt install -y python3-pip && pip3 install flask
COPY . /srv
WORKDIR /srv
CMD ["python3", "app.py"]
