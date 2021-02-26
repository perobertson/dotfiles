export EDITOR='vim'
export CODE_PATH="$HOME/workspace"
GPG_TTY=$(tty)
export GPG_TTY

# Configure less as the pager and reprint the screen when content changes
# Enables scrolling
export PAGER=less
export LESS=-R
