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

alias c='tput reset'
alias gitview='git log --oneline --decorate --graph --branches --tags'
