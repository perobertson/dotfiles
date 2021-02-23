export EDITOR='vim'
export CODE_PATH="$HOME/workspace"
GPG_TTY=$(tty)
export GPG_TTY

export PKENV_ROOT="$HOME/Applications/pkenv"
export PYENV_ROOT="$HOME/Applications/pyenv"
export TFENV_ROOT="$HOME/Applications/tfenv"
export RBENV_ROOT="$HOME/Applications/rbenv"

export GOPATH="$HOME/go"

# virtual environments will modify the path then reopen a shell
# this will make sure we do not clobber the virtual env path
if [[ "$DOTFILES_PATH" = '' ]]; then
    # Prefer python bins over system
    export PATH="$HOME/.local/bin:$PATH"

    # Prefer go bins over python
    export PATH="$GOPATH/bin:$PATH"

    # Prefer rust bins over go
    export PATH="$HOME/.cargo/bin:$PATH"

    # Prefer user bins over system
    export PATH="$HOME/bin:$PATH"

    # Prefer virtual envs over user bins
    export PATH="$RBENV_ROOT/bin:$PATH"
    export PATH="$TFENV_ROOT/bin:$PATH"
    export PATH="$PKENV_ROOT/bin:$PATH"
    export PATH="$PYENV_ROOT/bin:$PATH"

    export DOTFILES_PATH=1
fi

fpath=($HOME/.zsh/functions /usr/local/share/zsh/vendor-completions /usr/share/zsh/vendor-completions $fpath)

autoload -U $HOME/.zsh/functions/*(:t)

HISTFILE=~/.zsh_history
HISTSIZE=1000
SAVEHIST=1000
REPORTTIME=10 # print elapsed time when more than 10 seconds

setopt NO_BG_NICE # don't nice background tasks
setopt NO_HUP
setopt NO_LIST_BEEP
setopt LOCAL_OPTIONS # allow functions to have local options
setopt LOCAL_TRAPS # allow functions to have local traps
setopt HIST_VERIFY
setopt SHARE_HISTORY # share history between sessions ???
setopt EXTENDED_HISTORY # add timestamps to history
setopt PROMPT_SUBST
setopt CORRECT
setopt COMPLETE_IN_WORD
setopt IGNORE_EOF

setopt APPEND_HISTORY # adds history
setopt INC_APPEND_HISTORY SHARE_HISTORY  # adds history incrementally and share it across sessions
setopt HIST_IGNORE_ALL_DUPS  # don't record dupes in history
setopt HIST_REDUCE_BLANKS
setopt HIST_IGNORE_SPACE  # don't record commands that start with a space
setopt menu_complete

# Use 'bindkey' to list all bound keys
# Use 'cat -v' to discover the codes for key combinations
bindkey '^[[1;5C' forward-word  # ctrl+right
bindkey '^[[1;5D' backward-word  # ctrl+left
bindkey '^[[3~' delete-char  # delete
bindkey '^[[F' end-of-line  # end (fn+right)
bindkey '^[[H' beginning-of-line  # home (fn+left)