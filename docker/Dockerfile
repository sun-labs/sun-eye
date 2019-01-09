FROM nvcr.io/nvidia/cuda:9.0-devel-ubuntu16.04

WORKDIR /***REMOVED***

#
# OPENCV + CUDA SUPPORT
#
RUN apt-get update -y
RUN apt-get update

# GOOD STUFF
RUN apt-get install tmux -y
RUN apt-get install wget -y
RUN apt-get install psmisc -y
RUN apt-get install sudo -y

RUN apt-get install python3-dev -y
RUN apt-get install python3-pip -y

RUN apt-get install build-essential cmake unzip pkg-config -y
RUN apt-get install libjpeg-dev libpng-dev libtiff-dev -y
RUN apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev -y
RUN apt-get install libxvidcore-dev libx264-dev -y
RUN apt-get install libgtk-3-dev -y
RUN apt-get install libatlas-base-dev gfortran -y

RUN wget -O opencv.zip https://github.com/opencv/opencv/archive/4.0.1.zip
RUN wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.0.1.zip

RUN unzip opencv.zip
RUN unzip opencv_contrib.zip

RUN mv opencv-4.0.1 opencv
RUN mv opencv_contrib-4.0.1 opencv_contrib

RUN pip3 install numpy
WORKDIR opencv
RUN mkdir build
WORKDIR build
RUN cmake -D CMAKE_BUILD_TYPE=RELEASE \
	-D CMAKE_INSTALL_PREFIX=/usr/local \
	-D INSTALL_PYTHON_EXAMPLES=ON \
	-D INSTALL_C_EXAMPLES=OFF \
    -D WITH_CUDA=ON \
    -D WITH_CUBLAS=1 \
    -D CUDA_FAST_MATH=1 \
    -D CUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda \
	-D OPENCV_ENABLE_NONFREE=ON \
	-D OPENCV_EXTRA_MODULES_PATH=/***REMOVED***/opencv_contrib/modules \
	-D PYTHON_EXECUTABLE=/usr/bin/python3 \
	-D BUILD_EXAMPLES=ON ..

RUN make -j16
RUN make install
RUN ldconfig

# X11
RUN apt-get install xauth -y
RUN apt-get install x11-apps -y

# GTK MODULE
RUN apt-get install libcanberra-gtk-module -y
RUN apt-get install libcanberra-gtk3-module -y

RUN useradd -u 1001 -s /bin/bash ***REMOVED***

USER ***REMOVED***
#
# SSH SERVICE
#
# RUN apt-get update && apt-get install -y openssh-server
# RUN mkdir /var/run/sshd
# RUN echo 'root:screencast' | chpasswd
# RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# # SSH login fix. Otherwise user is kicked off after login
# RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

# ENV NOTVISIBLE "in users profile"
# RUN echo "export VISIBLE=now" >> /etc/profile

# EXPOSE 22
# CMD ["/usr/sbin/sshd", "-D"]

WORKDIR /***REMOVED***/development/
CMD NO_AT_BRIDGE=1 tmux