export HISTFILESIZE=5000000
export EDITOR='emacs'

if [[ "$OSTYPE" == "darwin"* ]]; then
    if [ -f ~/.bashrc ]; then . ~/.bashrc; fi
    export CC=gcc-7
    export CXX=g++-7
fi