if [ "$(uname)" == 'Darwin' ]; then
	alias ls='ls -G'
else
	alias ls='ls --color=auto'
	alias pbcopy='xsel --clipboard --input'
	alias pbpaste='xsel --clipboard --output'
fi

alias ll='ls -l'
cdls () {
	builtin cd "$@" && ls
}
alias cd='cdls'

alias c='tput reset'

