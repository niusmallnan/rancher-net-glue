FROM python:2.7
MAINTAINER niusmallnan <zhibo@rancher.com>

ENV SOURCE_REPO https://github.com/niusmallnan/rancher-net-glue.git

RUN mkdir /root/.pip
COPY .pip.aliyun.conf /root/.pip/pip.conf

RUN mkdir -p /app
WORKDIR /app

RUN git clone $SOURCE_REPO \
    && cd rancher-net-glue \
    && pip install --no-cache-dir -r requirements.txt \
    && python setup.py develop

CMD ["/bin/bash"]
