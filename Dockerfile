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
    wget \
    xdotool

# install, start elasticsearch: https://www.elastic.co/guide/en/elasticsearch/reference/current/deb.html#install-deb
RUN wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.7.1-amd64.deb && \
    wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.7.1-amd64.deb.sha512 && \
    shasum -a 512 -c elasticsearch-7.7.1-amd64.deb.sha512 && \
    sudo dpkg -i elasticsearch-7.7.1-amd64.deb && \
    rm elasticsearch-7.7.1-amd64.deb elasticsearch-7.7.1-amd64.deb.sha512

# link specific python version to "python"
RUN ln -s /usr/bin/python3.7 /usr/bin/python

# cd to tsar directory, install python deps, copy
ARG tsar_folder
ENV APP_PATH=$tsar_folder
WORKDIR $APP_PATH

COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt
ENV PYTHONPATH=$APP_PATH

# overwrite elasticsearch config file with host config file
COPY --chown=root:elasticsearch ./resources/elasticsearch/* /etc/elasticsearch/

# create executable alias in container
RUN ln -s $APP_PATH/tsar/app/app.py /usr/bin/tsar

# Add public key to known hosts
RUN mkdir -p /root/.ssh && \
    chmod 0700 /root/.ssh && \
    ssh-keyscan host.docker.internal >> /root/.ssh/known_hosts

CMD service elasticsearch start && /bin/bash
# RUN mkdir -p /Users/trensink/move_files_no_data/git/my_repos/tsar/resources/elasticsearch/logs
# RUN service elasticsearch start
