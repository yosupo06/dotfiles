#!/usr/bin/env zsh

THIS_DIR=$(cd $(dirname $0); pwd)

ADD_STR='. '$THIS_DIR'/profile'
FILE=~/.zprofile

if grep -sq ^$ADD_STR$ $FILE; then
    echo 'profile already added, skip'
else
    echo 'add profile'
    echo $ADD_STR >> $FILE
fi

ADD_STR='. '$THIS_DIR'/zshrc'
FILE=~/.zshrc

if grep -sq ^$ADD_STR$ $FILE; then
    echo 'zshrc already added, skip'
else
    echo 'add zshrc'
    echo $ADD_STR >> $FILE
fi

cp -r $THIS_DIR'/emacs.d/.' ~/.emacs.d/


#git config
git config --global user.name "Kohei Morita"
git config --global user.email yosupo06@gmail.com
git config --global credential.helper store

git config --global alias.st status
git config --global alias.cob 'checkout -b'
git config --global alias.sub submodule
git config --global alias.subup 'submodule update'
git config --global alias.view 'log --oneline --decorate --graph --branches --tags'
