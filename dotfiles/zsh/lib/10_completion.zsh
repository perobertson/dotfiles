autoload -U compinit
compinit

# use 'zstyle -L' to see all configured entries

# menu selecting
zstyle ':completion:*:*:*:*:*' menu select

# matches case insensitive for lowercase
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Z}'

# pasting with tabs doesn't perform completion
zstyle ':completion:*' insert-tab pending

# completion style for makefiles
zstyle ':completion:*:*:make:*' tag-order 'targets'

# Completions for pip
if [[ -x $(command -v pip) ]]; then
    compctl -K _pip_completion pip
fi
if [[ -x $(command -v pip3) ]]; then
    compctl -K _pip_completion pip3
fi

# Set up pyenv
if [[ -x "$(command -v pyenv)" ]]; then
  eval "$(pyenv init -)"
fi

# Set up rbenv
if [[ -x "$(command -v rbenv)" ]]; then
  eval "$(rbenv init -)"
fi

# Set up zoxide
if [[ -x "$(command -v zoxide)" ]]; then
  eval "$(zoxide init zsh)"
fi

# Set up aws completions (cli v1)
if [[ -x "$(command -v aws_zsh_completer.sh)" ]]; then
  source "$(command -v aws_zsh_completer.sh)"
fi

# Configure prompt
if [[ -x "$(command -v starship)" ]]; then
  eval "$(starship init zsh)"
fi
