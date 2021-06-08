export PKENV_ROOT="$HOME/Applications/pkenv"
export PYENV_ROOT="$HOME/Applications/pyenv"
export TFENV_ROOT="$HOME/Applications/tfenv"
export RBENV_ROOT="$HOME/Applications/rbenv"

export GOPATH="$HOME/go"

# virtual environments will modify the path then reopen a shell
# this will make sure we do not clobber the virtual env path
if [[ -z "${DOTFILES_PATH:-}" ]]; then
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
