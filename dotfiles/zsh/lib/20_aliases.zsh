# cd
alias ..='cd ..'

# ls
alias ls="ls -F --color=auto"
alias l="ls -lAh"
alias ll="ls -l"
alias la='ls -A'

if [ "$(command -v exa)" ]; then
    unalias -m 'ls'
    unalias -m 'l'
    unalias -m 'll'
    unalias -m 'la'
    alias ls='exa --color auto -s type -F'
    alias l="ls -laH"
    alias la="ls -a"
    alias ll="ls -l --git"
    alias lg="ls -lG"
    # Icons require a nerd font
    # https://www.nerdfonts.com/font-downloads
    alias li="ll --icons"
fi

if [ "$(command -v bat)" ]; then
  unalias -m 'cat'
  alias cat='bat -pp'
fi

# git
alias g='git'
alias ga='git add'
alias gb='git branch'
alias gc='git commit -m'
alias gca='git commit -a'
alias gcb='git checkout -b'
alias gcd='git checkout develop'
alias gcm='git checkout main || git checkout master'
alias gco='git checkout'
alias gd='git diff'
alias gdc='git diff --cached'
alias gdw='git diff --word-diff'
alias gf='git fetch'
alias gfa='git fetch --all --prune --prune-tags'
alias gk='\gitk --all --branches'
alias gl='git pull --rebase --stat'
alias glog='git log --oneline --decorate --color --graph'
alias gloga='git log --graph --decorate --oneline --color --all'
alias glogd='git log --graph --decorate $(git rev-list -g --all)'
alias gm='git merge'
alias gp='git push'
alias gr='git remote'
alias grb='git rebase'
alias grba='git rebase --abort'
alias grbc='git rebase --continue'
alias grbi='git rebase -i'
alias grbs='git rebase --skip'
alias grm="git status | grep deleted | awk '{print \$3}' | xargs git rm"
alias gs='git status'
alias gsc='git commit -S -m'
alias gss='git status --short'

# terraform
alias tf='terraform'

# other
alias aws-whoami="aws sts get-caller-identity"
alias fcd='cd "$(find . -type d -name '.git' | grep -v '\\\\.terraform' | sed s/\\.git// | fzf)"'
alias fsubl='subl "$(find . -type d -name '.git' | grep -v '\\\\.terraform' | sed s/\\.git// | fzf)"'
alias rsync="rsync --progress"
alias ssh-keygen='ssh-keygen -t ed25519'
alias tmux="TERM=screen-256color-bce tmux -2"
