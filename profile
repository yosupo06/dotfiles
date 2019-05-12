export HISTFILESIZE=5000000
export EDITOR='emacs'

THIS_DIR=$(dirname $BASH_SOURCE)

export PATH=$PATH:$THIS_DIR/competitive_scripts/


if [[ "$OSTYPE" == "darwin"* ]]; then
    if [ -f ~/.bashrc ]; then . ~/.bashrc; fi
    export CC=gcc-7
    export CXX=g++-7
fi