export HISTFILE=${HOME}/.zhistory
export HISTFILESIZE=5000000
export EDITOR='emacs'

THIS_DIR=$(dirname $0)

export PATH=$THIS_DIR/competitive_scripts:$THIS_DIR/scripts:$PATH
