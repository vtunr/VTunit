FROM vtunr/esp:latest

# Installing vtunit 
# Install CMake, compilers
RUN apt-get update && apt-get install -y git build-essential cmake ninja-build 

RUN apt-get install -y python
RUN apt-get install -y python-pip

# Ctags installation
RUN apt install -y \
    make \
    pkg-config autoconf automake \
    python3-docutils \
    libseccomp-dev \
    libjansson-dev \
    libyaml-dev \
    libxml2-dev

RUN mkdir ~/ctags/ && cd ~/ctags/ && git clone https://github.com/universal-ctags/ctags.git . && ./autogen.sh && ./configure && make install 

RUN mkdir -p vt && python2.7 -m pip install -e git+https://github.com/vtunr/VTunit.git#egg=VTunit --src /vt 

WORKDIR /project