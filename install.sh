#!/usr/bin/env bash

THIS_DIR=$(cd $(dirname $0); pwd)

ADD_STR='. '$THIS_DIR'/profile'
if [ -e ~/.profile ]; then
    FILE=~/.profile
else
    FILE=~/.bash_profile
fi

if grep -sq ^$ADD_STR$ $FILE; then
    echo 'profile already added, skip'
else
    echo 'add profile'
    echo $ADD_STR >> $FILE
fi

ADD_STR='. '$THIS_DIR'/bashrc'
FILE=~/.bashrc

if grep -sq ^$ADD_STR$ $FILE; then
    echo 'bashrc already added, skip'
else
    echo 'add bashrc'
    echo $ADD_STR >> $FILE
fi

cp -r $THIS_DIR'/emacs.d/.' ~/.emacs.d/


#git config
git config --global user.name "Kohei Morita"
git config --global user.email yosupo06@gmail.com
git config --global credential.helper 'cache --timeout=3600'

git config --global alias.st status
git config --global alias.cob 'checkout -b'
git config --global alias.sub submodule
git config --global alias.subup 'submodule update'
git config --global alias.view 'log --oneline --decorate --graph --branches --tags'
