alias ls='ls -G'
alias ll='ls -l'
cdls () {
	builtin cd "$@" && ls
}
alias cd='cdls'

# git

alias gitview='git log --oneline --decorate --graph --branches --tags --remotes'
