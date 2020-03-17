if [[ "$(uname)" == 'Darwin' ]]; then
	alias ls='ls -G'
else
	alias ls='ls --color=auto'
	alias pbcopy='xsel --clipboard --input'
	alias pbpaste='xsel --clipboard --output'
	alias open='xdg-open'
	alias c='tput reset'
fi

alias ll='ls -l'
cdls () {
	builtin cd "$@" && ls
}
alias cd='cdls'

autoload -Uz compinit
compinit

autoload -U promptinit
autoload -U colors && colors
local p_color="%(?.%{${fg[cyan]}%}.%{${fg[magenta]}%})"
if [[ "$(uname)" == 'Darwin' ]]; then
	PROMPT="${p_color}[%?]%{${reset_color}%}[%~]
🐟: "
else
	PROMPT="${p_color}[%?]%{${reset_color}%}[%~]
🐙: "
fi
