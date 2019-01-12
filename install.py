#!/usr/bin/env python3
# coding: utf-8
"""Setup script for installing dotfiles on a new computer."""

from __future__ import generator_stop

import getopt
import logging
import subprocess
import sys
from pathlib import Path

log = logging.getLogger(__name__)


def _help():
    """Print the help message."""
    print('install.py [-h|--help] [-v|--verbose] [--dry-run]')


def _verbose_logging():
    log.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)


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


def _install_configs(script, dry_run=False):
    """Create symlinks in the home config to the dotfiles project.

    This will only create symlinks for files to avoid pulling in additional configs.
    """
    def sync_dir(config_dir, target_dir):
        # make sure the directory exists in the home path
        config_dir.mkdir(parents=True, exist_ok=True)

        for target in target_dir.iterdir():
            if target.is_dir():
                sync_dir(config_dir.joinpath(target.name), target)
            elif target.is_file():
                config_file = config_dir.joinpath(target.name)

                is_file = config_file.is_file()
                is_link = config_file.is_symlink()
                is_same = (is_file or is_link) and config_file.samefile(target)

                msg = "file://{}\n  is_file:{}\n  is_symlink:{}\n  samefile:{}".format(
                    config_file,
                    is_file,
                    is_link,
                    is_same,
                )
                log.debug(msg)

                if not is_same:
                    if is_file:
                        backup_uri = "{}.bak".format(config_file.resolve())
                        backup_path = Path(backup_uri)
                        log.info("Creating backup: {}".format(backup_path))
                        if not dry_run:
                            config_file.replace(backup_path)
                    log.info("Creating link: {} -> {}".format(config_file, target))
                    if not dry_run:
                        config_file.symlink_to(target, target_is_directory=target.is_dir())

    config_dir = Path('~').joinpath('.config').expanduser()
    target_configs = script.parent.joinpath('config')
    sync_dir(config_dir, target_configs)


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
        opts, args = getopt.getopt(argv, 'hv', ['dry-run', 'help', 'verbose'])
    except getopt.GetoptError as e:
        log.error(e)
        _help()
        sys.exit(1)

    # init logging first
    for opt, arg in opts:
        if opt == '-v' or opt == '--verbose':
            _verbose_logging()

    dry_run = False
    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            _help()
            sys.exit(0)
        elif opt == '--dry-run':
            dry_run = True

    _fetch_submodules(script, dry_run=dry_run)
    _install_dotfiles(script, dry_run=dry_run)
    _install_oh_my_zsh(script, dry_run=dry_run)
    _install_configs(script, dry_run=dry_run)


if __name__ == '__main__':
    script_path = Path(sys.argv[0])
    main(script_path.resolve(), sys.argv[1:])
