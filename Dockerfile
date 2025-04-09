FROM osrf/ros:melodic-desktop-full

# 필수 패키지 설치 및 Python 3.8 설치
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    build-essential \
    git \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libffi-dev \
    liblzma-dev \
    tk-dev \
    sudo \
    libopencv-dev \
    python3.6 \
    python3.6-dev \
    python3.7 \
    python3.7-dev \
    python3-pip \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1 \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 2 \
    && update-alternatives --set python3 /usr/bin/python3.7 \
    && ln -sf /usr/bin/pip3 /usr/bin/pip

# pip 업그레이드 및 파이썬 패키지 설치
RUN pip install --upgrade pip && \
    pip install numpy opencv-python neo4j

# ROS 환경 설정
SHELL ["/bin/bash", "-c"]
RUN echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc


# 작업 디렉토리 생성
WORKDIR /root/catkin_ws

# Catkin 워크스페이스 초기화
RUN /bin/bash -c "source /opt/ros/melodic/setup.bash && \
    mkdir -p src && \
    cd src && \
    catkin_init_workspace && \
    cd .. && \
    catkin_make"

# ROS 환경 변수 설정
RUN echo "source /root/catkin_ws/devel/setup.bash" >> ~/.bashrc

# 기본 명령어
CMD ["/bin/bash"]


