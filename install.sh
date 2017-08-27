#!/usr/bin/env bash

THIS_DIR=$(cd $(dirname $0); pwd)

echo '.' $THIS_DIR'/profile' >> ~/.bash_profile #install bash_profile
echo '.' $THIS_DIR'/bashrc' >> ~/.bashrc #install bashrc
cp -r $THIS_DIR'/emacs.d' ~/.emacs.d


