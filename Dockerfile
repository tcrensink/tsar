FROM ubuntu:18.04

# command line tools
RUN apt-get update && \
    apt-get install -y \
    binutils \
    dpkg \
    git \
    iputils-ping \
    less \
    python3.7 \
    python3-pip \
    sudo \
    wget \
    xdotool

# install, start elasticsearch: https://www.elastic.co/guide/en/elasticsearch/reference/current/deb.html#install-deb
RUN wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.7.1-amd64.deb && \
    wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.7.1-amd64.deb.sha512 && \
    shasum -a 512 -c elasticsearch-7.7.1-amd64.deb.sha512 && \
    sudo dpkg -i elasticsearch-7.7.1-amd64.deb

# link specific python version to "python"
RUN ln -s /usr/bin/python3.7 /usr/bin/python

# cd to "/opt", install python deps, copy
WORKDIR /opt
COPY ./requirements.txt .
RUN python -m pip install -r requirements.txt
COPY . .
ENV PYTHONPATH="."

ENV PORT=9200
EXPOSE 9200
# create executable alias
RUN ln -s /opt/tsar/app/app.py /usr/bin/tsar

CMD ["tsar"]
