# Base image
FROM ubuntu:18.04

# Install CMake, compilers
RUN apt-get update && apt-get install -y git build-essential make ninja-build 
RUN apt-get install -y wget

ARG CMAKE_VERSION=3.22.1

RUN wget https://github.com/Kitware/CMake/releases/download/v${CMAKE_VERSION}/cmake-${CMAKE_VERSION}-Linux-x86_64.sh \
      -q -O /tmp/cmake-install.sh \
      && chmod u+x /tmp/cmake-install.sh \
      && mkdir /usr/bin/cmake \
      && /tmp/cmake-install.sh --skip-license --prefix=/usr/bin/cmake \
      && rm /tmp/cmake-install.sh

RUN apt-get install -y python
RUN apt-get install -y python-pip

# Ctags installation
RUN apt install -y \
    pkg-config autoconf automake \
    python3-docutils \
    libseccomp-dev \
    libjansson-dev \
    libyaml-dev \
    libxml2-dev

RUN mkdir ~/ctags/ && cd ~/ctags/ && git clone https://github.com/universal-ctags/ctags.git . && ./autogen.sh && ./configure && make install 

RUN mkdir -p ~/vt && python2.7 -m pip install -e git+https://github.com/vtunr/VTunit.git#egg=VTunit --src ~/vt 

ENV PATH="/usr/bin/cmake/bin:${PATH}"

WORKDIR /project