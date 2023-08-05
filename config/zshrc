export HISTSIZE=100000
export SAVEHIST=100000
export HISTFILE=~/.zsh_history

setopt hist_ignore_dups

get_os () {
	if [[ "$(uname)" == 'Darwin' ]]; then
		echo "MAC"
		return
	fi

	if [[ $(uname -r | sed -n 's/.*\( *Microsoft *\).*/\1/ip') ]]; then
		echo "WSL"
		return
	fi

	echo "Ubuntu"
	return
}

OS=`get_os`

echo "OS detected: ${OS}"

if [[ $OS == "MAC" ]]; then
	alias ls='ls -G'
else
	alias ls='ls --color=auto'
	alias c='tput reset'
fi

if [[ $OS == "Ubuntu" ]]; then
	alias pbcopy='xsel --clipboard --input'
	alias pbpaste='xsel --clipboard --output'
	alias open='xdg-open'
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

fix_wsl2_interop () {
    for i in $(pstree -np -s $$ | grep -o -E '[0-9]+'); do
        if [[ -e "/run/WSL/${i}_interop" ]]; then
            export WSL_INTEROP=/run/WSL/${i}_interop
        fi
    done
}

if [[ $OS == "WSL" ]]; then
	fix_wsl2_interop
fi
