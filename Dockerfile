FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y git-all

RUN apt-get install -y cmake
RUN apt-get install -y g++
RUN apt-get install -y libsdl1.2-dev
RUN git clone https://github.com/miyosuda/Arcade-Learning-Environment.git ~/Arcade-Learning-Environment
WORKDIR /root/Arcade-Learning-Environment
RUN cmake -DUSE_SDL=ON -DUSE_RLGLUE=OFF -DBUILD_EXAMPLES=OFF .
RUN make -j 4
RUN apt-get install -y python-pip
RUN pip install pip --upgrade
RUN pip install .

WORKDIR /root
ADD . /root/async_deep_reinforce
WORKDIR /root/async_deep_reinforce
RUN apt-get install -y python-opencv
RUN pip install -r requirements.txt

# personal
RUN apt-get install -y vim

ENTRYPOINT python a3c.py
