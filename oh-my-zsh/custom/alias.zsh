alias c='tput reset'

# brew install coreutils installs gls, which doesn't show color by -G
if command -v gls &> /dev/null; then
  alias ls="gls --color=always"
fi
