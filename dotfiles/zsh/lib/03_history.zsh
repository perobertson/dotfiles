# `man zshoptions` has the information about the history options
HISTFILE=${HOME}/.zsh_history
HISTSIZE=10000
SAVEHIST=10000

setopt EXTENDED_HISTORY # add timestamps to history
setopt HIST_EXPIRE_DUPS_FIRST  # expire oldest duplicate first
setopt HIST_FIND_NO_DUPS  # skip duplicates when searching history
setopt HIST_IGNORE_ALL_DUPS  # don't record dupes in history
setopt HIST_IGNORE_SPACE  # don't record commands that start with a space
setopt HIST_REDUCE_BLANKS  # removes extra spaces before appending to history
setopt HIST_VERIFY  # don't execute history expansion directly. Place into next command line for verification (!$)
setopt SHARE_HISTORY # adds history incrementally and loads new commands. Allows multiple terminals
