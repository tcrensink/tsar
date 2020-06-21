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

# cd to "/opt", install python deps, copy
ENV APP_PATH=/opt
WORKDIR $APP_PATH
COPY ./requirements.txt .
RUN python -m pip install -r requirements.txt
COPY . .
ENV PYTHONPATH=$APP_PATH

# # overwrite elasticsearch config file with host config file
COPY --chown=root:elasticsearch ./resources/elasticsearch/* /etc/elasticsearch/

# # ENV PORT=9200
# # EXPOSE 9200
# # create executable alias
RUN ln -s /opt/tsar/app/app.py /usr/bin/tsar

# set up credentials for ssh tunneling to host
ENV KEY_FOLDER="/opt/.ssh"
ENV KEY_PATH="$KEY_FOLDER/id_rsa"
RUN eval "$(ssh-agent -s)" && ssh-add $KEY_PATH && \
    ssh-keyscan -H host.docker.internal >> /opt/.ssh/known_hosts && \
    ln -s  /opt/.ssh /root/.ssh

# CMD ["tsar"]
