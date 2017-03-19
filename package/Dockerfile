FROM python:2.7
MAINTAINER niusmallnan <zhibo@rancher.com>

ENV SOURCE_REPO https://github.com/niusmallnan/rancher-net-glue.git

RUN mkdir /root/.pip
COPY .pip.aliyun.conf /root/.pip/pip.conf
COPY .jessie.source.list /etc/apt/sources.list

RUN mkdir -p /app
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
        git \
        && rm -rf /var/lib/apt/lists/* \
        && git clone $SOURCE_REPO \
        && cd rancher-net-glue \
        && pip install --no-cache-dir -r requirements.txt \
        && python setup.py develop

CMD ["/bin/bash"]
