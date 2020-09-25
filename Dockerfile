# This is a sample Dockerfile you can modify to deploy your own app based on face_recognition

FROM debian:stretch

RUN apt-get -y update
RUN apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-pip \
    python3-numpy \
    python3-setuptools \
    software-properties-common \
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

RUN cd ~ && \
    mkdir -p dlib && \
    git clone -b 'v19.9' --single-branch https://github.com/davisking/dlib.git dlib/ && \
    cd  dlib/ && \
    python3 setup.py install --yes USE_AVX_INSTRUCTIONS

COPY . /root/face_recognition
RUN cd /root/face_recognition && \
    pip3 install -r requirements.txt && \
    python3 setup.py install

# install OpenCV # libjasper-dev
RUN apt-get install -y \
    python-dev python-numpy python3-dev python3-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libdc1394-22-dev \
    libv4l-dev libxvidcore-dev libx264-dev libgtk-3-dev libatlas-base-dev pylint unzip

RUN wget https://github.com/opencv/opencv/archive/3.4.0.zip -O opencv-3.4.0.zip
RUN wget https://github.com/opencv/opencv_contrib/archive/3.4.0.zip -O opencv_contrib-3.4.0.zip

RUN unzip opencv-3.4.0.zip
RUN unzip opencv_contrib-3.4.0.zip
RUN cd opencv-3.4.0 && \
    mkdir build
RUN cd opencv-3.4.0/build && \
    cmake \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_PREFIX=/usr/local \
        -DOPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-3.4.0/modules \
        -DOPENCV_ENABLE_NONFREE=True \
        #-DPYTHON_DEFAULT_EXECUTABLE=$(which python3) \
        .. && \
    make -j4 && \ 
    make install && \
    ldconfig

# The rest of this file just runs an example script.

# If you wanted to use this Dockerfile to run your own app instead, maybe you would do this:
# COPY . /root/your_app_or_whatever
# RUN cd /root/your_app_or_whatever && \
#     pip3 install -r requirements.txt
# RUN whatever_command_you_run_to_start_your_app

#CMD cd /root/face_recognition/examples && \
#    python3 recognize_faces_in_pictures.py
