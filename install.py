#!/usr/bin/env python3
# coding: utf-8
"""Setup script for installing dotfiles on a new computer."""

from __future__ import generator_stop

import getopt
import subprocess
import sys
from pathlib import Path


def _short_help():
    """Print the help message and exits."""
    print('install.py [-h] [--dry-run]')
    sys.exit(2)


def _long_help():
    _short_help()


def _link_file(link, target, dry_run=False, backup=False):
    """Create a symlink at link to target.

    :param link:    the name of the link to create
    :type link:     pathlib.Path
    :param target:  the target that the link points to
    :type target:   pathlib.Path
    """
    print("linking file '{}' -> '{}'".format(link, target))
    if not dry_run:
        if backup:
            link_uri = link.resolve()
            backup_uri = "{}.bak".format(link_uri)
            print("created backup '{}'".format(backup_uri))
            link.replace(backup_uri)
        link.symlink_to(target, target_is_directory=target.is_dir())


def _install_gitconfig(script, dry_run=False):
    """Install the global gitconfig file.

    This file is special because we want some sections to be untracked.
    Use include to handle this case https://git-scm.com/docs/git-config#_includes
    """
    global_config_file = Path('~').joinpath('.gitconfig').expanduser()
    source_config_file = script.parent.joinpath('dotfiles').joinpath('gitconfig')
    include_path = "path = {}".format(source_config_file.resolve())
    new_content = "[include]\n\t{}".format(include_path)

    if global_config_file.exists():
        print('global gitconfig exists')
        with global_config_file.open() as f:
            content = f.read()
        if include_path not in content:
            print("\tappending include section")
            if not dry_run:
                with global_config_file.open(mode='a') as f:
                    print(new_content, file=f)
    else:
        print("creating {}".format(global_config_file))
        if not dry_run:
            with global_config_file.open(mode='w') as f:
                print(new_content, file=f)


def _install_dotfiles(script, dry_run=False):
    """Install the dotfiles.

    :param script: Path object to this file
    :type script: pathlib.Path
    :param dry_run: True if the commands should be displayed instead of executed
    """
    to_skip = {
        '.git',
        '.gitignore',
        '.gitmodules',
        'gitconfig',
        'install.py',
        'LICENSE',
        'Rakefile',
        'README.md',
        'README.rdoc',
    }
    script.joinpath
    dotfiles = script.parent.joinpath('dotfiles')
    for f in dotfiles.iterdir():
        if f.name in to_skip:
            print("skipping: {}".format(f.name))
            continue
        home_dir_file = Path('~').joinpath(".{}".format(f.name)).expanduser()
        if home_dir_file.exists():
            if f.samefile(home_dir_file):
                print("identical {}".format(home_dir_file))
            else:
                _link_file(home_dir_file, f, dry_run=dry_run, backup=True)
        else:
            _link_file(home_dir_file, f, dry_run=dry_run)
    _install_gitconfig(script, dry_run=dry_run)


def _install_oh_my_zsh(script, dry_run=False):
    zsh_path = Path('~/.oh-my-zsh').expanduser()
    if zsh_path.exists():
        print("oh-my-zsh is already installed")
        return

    print("Installing oh-my-zsh")
    if not dry_run:
        cmd = 'git clone https://github.com/robbyrussell/oh-my-zsh.git "$HOME/.oh-my-zsh"'
        subprocess.run(cmd, shell=True, check=True)


def _fetch_submodules(script, dry_run=False):
    if dry_run:
        print('git submodule init')
        print('git submodule update')
    else:
        cwd = str(script.parent.resolve())
        subprocess.run('git submodule init', shell=True, check=True, cwd=cwd)
        subprocess.run('git submodule update', shell=True, check=True, cwd=cwd)


def main(script, argv):
    """Install the dotfiles and initialize submodules."""
    try:
        opts, args = getopt.getopt(argv, 'h', ['help', 'dry-run'])
    except getopt.GetoptError:
        _short_help()

    dry_run = False
    for opt, arg in opts:
        if opt == '-h':
            _short_help()
        elif opt == '--help':
            _long_help()
        elif opt == '--dry-run':
            dry_run = True

    _fetch_submodules(script, dry_run=dry_run)
    _install_dotfiles(script, dry_run=dry_run)
    _install_oh_my_zsh(script, dry_run=dry_run)


if __name__ == '__main__':
    script_path = Path(sys.argv[0])
    main(script_path.resolve(), sys.argv[1:])
