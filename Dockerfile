# Docker file for libav ChRIS plugin app
#
# Build with
#
#   docker build -t <name> .
#
# For example if building a local version, you could do:
#
#   docker build -t local/pl-libav .
#
# In the case of a proxy (located at 192.168.13.14:3128), do:
#
#    docker build --build-arg http_proxy=http://192.168.13.14:3128 --build-arg UID=$UID -t local/pl-libav .
#
# To run an interactive shell inside this container, do:
#
#   docker run -ti --entrypoint /bin/bash local/pl-libav
#
# To pass an env var HOST_IP to container, do:
#
#   docker run -ti -e HOST_IP=$(ip route | grep -v docker | awk '{if(NF==11) print $9}') --entrypoint /bin/bash local/pl-libav
#

FROM python:3.9.1-slim-buster
LABEL maintainer="slegendr <slegendr@redhat.com>"

WORKDIR /usr/local/src

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN pip install .
RUN pip install pydicom
RUN pip install pillow
RUN pip install numpy

#libav-tools is not available in docker, so build libav from source
RUN apt-get -y update
RUN apt-get -y install gcc git make pkg-config yasm
RUN git clone https://github.com/libav/libav.git libav_git
RUN ./libav_git/configure
RUN make; make install;

CMD ["libav", "--help"]
