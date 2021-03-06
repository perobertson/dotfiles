# Paul Robertson Dot Files

These are config files to set up a system the way I like it.

## Installation

```bash
git clone https://gitlab.com/perobertson/dotfiles.git ~/.dotfiles
cd ~/.dotfiles
./install.py
```

## Environment

I primarily use Linux with `zsh` as my shell.
To switch to zsh, you can do so with the following command.

```bash
chsh -s "$(command -v zsh)"
```

## Features

I normally place all of my coding projects in `~/workspace`.
This directory can easily be accessed (and tab completed) with the "c" command.
This can be configured by exporting `CODE_PATH` from the .localrc file.

```text
c re<tab>
```

There is also an "h" command which behaves similar, but acts on the
home path.

```text
h doc<tab>
```

Tab completion is also added to rake and cap commands:

```text
rake db:mi<tab>
cap de<tab>
```

To speed things up, the results are cached in local `.rake_tasks~` and
`.cap_tasks~`. It is smart enough to expire the cache automatically in
most cases, but you can simply remove the files to flush the cache.

There are a few key bindings set. Many of these require option to be
set as the meta key. Option-left/right arrow will move cursor by word,
and control-left/right will move to beginning and end of line.
Control-option-N will open a new tab with the current directory under
Mac OS X Terminal.

If you're using git, you'll notice the current branch name shows up in
the prompt while in a git repository.

See the other aliases in `~/.zsh/aliases`

If there are some shell configuration settings which you want secure or
specific to one system, place it into a `~/.localrc` file. This will be
loaded automatically if it exists.

There are several features enabled in Ruby's irb including history and
completion. Many convenience methods are added as well such as "ri"
which can be used to get inline documentation in IRB. See `irbrc` and
`railsrc` files for details.
