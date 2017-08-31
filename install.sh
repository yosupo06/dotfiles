#!/usr/bin/env bash

THIS_DIR=$(cd $(dirname $0); pwd)

if [ -e ~/.profile ]; then
    echo '.' $THIS_DIR'/profile' >> ~/.profile #install bash_profile
else
    echo '.' $THIS_DIR'/profile' >> ~/.bash_profile #install bash_profile
fi

echo '.' $THIS_DIR'/bashrc' >> ~/.bashrc #install bashrc
cp -r $THIS_DIR'/emacs.d/.' ~/.emacs.d/


#git config
git config --global user.name "Kohei Morita"
git config --global user.email yosupo06@gmail.com
