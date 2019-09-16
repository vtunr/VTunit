# Base image
FROM ubuntu:18.04

RUN apt-get update && apt-get install -y ruby gcc
RUN gem install ceedling

# Install CMake, compilers, GTest and GMock
RUN apt-get update && apt-get install -y git build-essential cmake ninja-build libgtest-dev google-mock 

RUN apt-get install -y python
RUN apt-get install -y python-pip
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

RUN pip3 install docker

RUN apt install -y \
    make \
    pkg-config autoconf automake \
    python3-docutils \
    libseccomp-dev \
    libjansson-dev \
    libyaml-dev \
    libxml2-dev

RUN mkdir ~/ctags/ && cd ~/ctags/ && git clone https://github.com/universal-ctags/ctags.git . && ./autogen.sh && ./configure && make install 


WORKDIR /tmp/project
