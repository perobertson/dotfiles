export PKENV_ROOT="$HOME/Applications/pkenv"
export PYENV_ROOT="$HOME/Applications/pyenv"
export TFENV_ROOT="$HOME/Applications/tfenv"
export RBENV_ROOT="$HOME/Applications/rbenv"

export GOPATH="$HOME/go"

# virtual environments will modify the path then reopen a shell
# this will make sure we do not clobber the virtual env path
if [[ -z "${DOTFILES_PATH:-}" ]]; then
    # Prefer python bins over system
    if [[ -d "$HOME/.local/bin" ]]; then
        export PATH="$HOME/.local/bin:$PATH"
    fi

    # Prefer go bins over python
    if [[ -d "$GOPATH/bin" ]]; then
        export PATH="$GOPATH/bin:$PATH"
    fi

    # Prefer rust bins over go
    if [[ -d "$HOME/.cargo/bin" ]]; then
        export PATH="$HOME/.cargo/bin:$PATH"
    fi

    # Prefer user bins over system
    if [[ -d "$HOME/bin" ]]; then
        export PATH="$HOME/bin:$PATH"
    fi

    # Prefer virtual envs over user bins
    if [[ -d "$RBENV_ROOT/bin" ]]; then
        export PATH="$RBENV_ROOT/bin:$PATH"
    fi
    if [[ -d "$TFENV_ROOT/bin" ]]; then
        export PATH="$TFENV_ROOT/bin:$PATH"
    fi
    if [[ -d "$PKENV_ROOT/bin" ]]; then
        export PATH="$PKENV_ROOT/bin:$PATH"
    fi
    if [[ -d "$PYENV_ROOT/bin" ]]; then
        export PATH="$PYENV_ROOT/bin:$PATH"
    fi

    # Set up rbenv
    if [[ -x "$(command -v rbenv)" ]]; then
        eval "$(rbenv init -)"
    fi

    # Set up pyenv
    if [[ -x "$(command -v pyenv)" ]]; then
        eval "$(pyenv init --path)"
    fi

    # Flag to prevent resetting the path in a subshell
    export DOTFILES_PATH=1
fi
