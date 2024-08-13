#!/usr/bin/env bash

cp oh-my-zsh/custom/alias.zsh $HOME/.oh-my-zsh/custom
cp oh-my-zsh/custom/export.zsh $HOME/.oh-my-zsh/custom

if [ "$REMOTE_CONTAINERS" != "true" ]; then
    git config --global user.name "Kohei Morita"
    git config --global user.email "yosupo06@gmail.com"

    git config --global alias.st "status"
    git config --global alias.cob "checkout -b"
fi
