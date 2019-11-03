export HISTFILESIZE=5000000
export EDITOR='emacs'

THIS_DIR=$(dirname $BASH_SOURCE)

export PATH=$THIS_DIR/competitive_scripts:$THIS_DIR/scripts:$PATH


if [[ "$OSTYPE" == "darwin"* ]]; then
    if [ -f ~/.bashrc ]; then . ~/.bashrc; fi
#    export CC=gcc-9
    export CXX=g++-9
fi
