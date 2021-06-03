FROM ubuntu:18.04

# command line tools
RUN apt-get update && \
    apt-get install -y \
    binutils \
    curl \
    dpkg \
    git \
    iputils-ping \
    less \
    nano \
    python3.7 \
    python3-pip \
    sudo \
    wget

# install, start elasticsearch: https://www.elastic.co/guide/en/elasticsearch/reference/current/deb.html#install-deb
RUN sudo apt update && apt install apt-transport-https
RUN apt install -y openjdk-8-jdk
RUN wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
RUN sudo sh -c 'echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" > /etc/apt/sources.list.d/elastic-7.x.list'
RUN sudo apt update && sudo apt install -y elasticsearch

# link specific python version to "python"
RUN ln -s /usr/bin/python3.7 /usr/bin/python && python -m pip install --upgrade pip && python -m pip install --upgrade setuptools

# expose cli client, es ports:
EXPOSE 8137
EXPOSE 8138

# copy requirements, creat python path
WORKDIR $APP_PATH
COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt
ENV PYTHONPATH=$APP_PATH

# overwrite elasticsearch config file with host config file
COPY --chown=root:elasticsearch ./resources/elasticsearch/elasticsearch.yml /etc/elasticsearch/elasticsearch.yml

# create executable alias in container
RUN ln -s $APP_PATH/tsar/app/app.py /usr/bin/tsar
