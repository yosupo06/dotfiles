if [ "$(uname)" == 'Darwin' ]; then
	alias ls='ls -G'
else
	alias ls='ls --color=auto'
fi

alias ll='ls -l'
cdls () {
	builtin cd "$@" && ls
}
alias cd='cdls'

# git

alias gitview='git log --oneline --decorate --graph --branches --tags --remotes'
