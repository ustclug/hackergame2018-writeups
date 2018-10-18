FROM ubuntu:artful
MAINTAINER SIYUAN-ZHUANG USTC-1411
ENV LC_ALL=C.UTF-8

RUN apt-get update
RUN apt-get install --yes python3.6 python3.6-dev python3-pip python3-openssl
COPY ./webapp /webapp
WORKDIR /webapp
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["webapp.py"]
