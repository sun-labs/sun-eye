FROM nvcr.io/nvidia/cuda:9.0-devel-ubuntu16.04

RUN apt-get update -y
RUN apt-get update
RUN apt-get install tmux -y

WORKDIR /***REMOVED***

ADD install-cv.sh .
RUN chmod +x install-cv.sh
RUN ./install-cv.sh

CMD tmux