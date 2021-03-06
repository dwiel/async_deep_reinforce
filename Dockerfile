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

# for tinyik virtual arm environment
RUN apt-get install -y libblas-dev liblapack-dev libatlas-base-dev gfortran

# personal
RUN apt-get install -y vim

RUN git clone https://github.com/dwiel/dotfiles.git
RUN ln dotfiles/.vimrc .
RUN ln dotfiles/.style.yapf .

# bash git completion
RUN apt-get install -y git-core bash-completion
RUN echo "" >> ~/.bashrc
RUN echo "if [ -f /etc/bash_completion ] && ! shopt -oq posix; then" >> ~/.bashrc
RUN echo "    . /etc/bash_completion" >> ~/.bashrc
RUN echo "fi" >> ~/.bashrc

# setup git config options
RUN git config --global user.email "zdwiel@gmail.com"
RUN git config --global user.name "Zach Dwiel"
RUN git config --global push.default current

# install vim plugins
RUN apt-get install -y curl
RUN mkdir -p ~/.vim/autoload ~/.vim/bundle && curl -LSso ~/.vim/autoload/pathogen.vim https://tpo.pe/pathogen.vim
RUN curl -fLo ~/.vim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
RUN vim +PlugInstall +qall

# yapf needed for vim plugins
RUN pip install yapf

# basic requirements
RUN apt-get install -y python-opencv
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
ADD . /root/async_deep_reinforce
WORKDIR /root/async_deep_reinforce

CMD python a3c.py


