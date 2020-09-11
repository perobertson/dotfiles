#!/usr/bin/env python3
# coding: utf-8
"""Setup script for installing dotfiles on a new computer."""
from __future__ import generator_stop

import argparse
import logging
import subprocess
import sys
from pathlib import Path
from typing import Optional

try:
    from termcolor import colored
    maybe_colored = colored
except ImportError:
    def maybe_colored(
        text: str,
        color: Optional[str] = None,
        on_color: Optional[str] = None,
        attrs: Optional[str] = None,
    ) -> str:
        """Return the text without colouring it."""
        return text

FORMAT = maybe_colored(
    '%(asctime)-s %(levelname)-8s %(filename)s:%(lineno)s',
    'cyan'
) + maybe_colored(
    ' %(funcName)s',
    'yellow'
) + ' %(message)s'
logging.basicConfig(format=FORMAT)
log = logging.getLogger(__name__)


def _help():
    """Print the help message."""
    print('install.py [-h|--help] [-v|--verbose] [--dry-run]')


def _link_file(link, target, dry_run=False, backup=False):
    """Create a symlink at link to target.

    :param link:    the name of the link to create
    :type link:     pathlib.Path
    :param target:  the target that the link points to
    :type target:   pathlib.Path
    """
    log.info(f"linking file '{link}' -> '{target}'")
    if not dry_run:
        if backup:
            link_uri = link.resolve()
            backup_uri = f"{link_uri}.bak"
            log.info(f"created backup '{backup_uri}'")
            link.replace(backup_uri)
        link.symlink_to(target, target_is_directory=target.is_dir())


def _install_gitconfig(script, dry_run=False):
    """Install the global gitconfig file.

    This file is special because we want some sections to be untracked.
    Use include to handle this case https://git-scm.com/docs/git-config#_includes
    """
    global_config_file = Path('~').joinpath('.gitconfig').expanduser()
    source_config_file = script.parent.joinpath('dotfiles').joinpath('gitconfig')
    include_path = f"path = {source_config_file.resolve()}"
    new_content = f"[include]\n\t{include_path}"

    if global_config_file.exists():
        log.debug('global gitconfig exists')
        with global_config_file.open() as f:
            content = f.read()
        if include_path not in content:
            log.info("\tappending include section")
            if not dry_run:
                with global_config_file.open(mode='a') as f:
                    print(new_content, file=f)
    else:
        log.info(f"creating {global_config_file}")
        if not dry_run:
            with global_config_file.open(mode='w') as f:
                print(new_content, file=f)


def _install_dotfiles(script, dry_run=False):
    """Install the dotfiles.

    :param script: Path object to this file
    :type script: pathlib.Path
    :param dry_run: True if the commands should be displayed instead of executed
    """
    log.info('Installing dotfiles')
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
            log.debug(f"skipping: {f.name}")
            continue
        home_dir_file = Path('~').joinpath(f".{f.name}").expanduser()
        if home_dir_file.exists():
            if f.samefile(home_dir_file):
                log.debug(f"identical {home_dir_file}")
            else:
                _link_file(home_dir_file, f, dry_run=dry_run, backup=True)
        else:
            _link_file(home_dir_file, f, dry_run=dry_run)
    _install_gitconfig(script, dry_run=dry_run)


def _link_files(local_dir: Path, target_dir: Path, dry_run: bool = False) -> None:
    """Link files in the local dir to the target dir.

    This will only create symlinks for files to avoid pulling in additional configs.
    """
    # make sure the directory exists in the home path
    local_dir.mkdir(parents=True, exist_ok=True)

    for target in target_dir.iterdir():
        if target.is_dir():
            _link_files(local_dir.joinpath(target.name), target, dry_run)
        elif target.is_file():
            config_file = local_dir.joinpath(target.name)

            is_file = config_file.is_file()
            is_link = config_file.is_symlink()
            is_same = (is_file or is_link) and config_file.samefile(target)

            msg = f"file://{config_file}\n  is_file:{is_file}\n  is_symlink:{is_link}\n  samefile:{is_same}"
            log.debug(msg)

            if is_same:
                continue

            if is_file:
                backup_uri = f"{config_file.resolve()}.bak"
                backup_path = Path(backup_uri)
                log.info(f"Creating backup: {backup_path}")
                if not dry_run:
                    config_file.replace(backup_path)
            log.info(f"Creating link: {config_file} -> {target}")
            if not dry_run:
                config_file.symlink_to(target, target_is_directory=target.is_dir())


def _install_configs(script, dry_run=False):
    """Create symlinks in the home config to the dotfiles project."""
    log.info('Installing .config')
    config_dir = Path('~').joinpath('.config').expanduser()
    target_configs = script.parent.joinpath('config')
    _link_files(config_dir, target_configs, dry_run=dry_run)


def _install_ssh_config(script, dry_run=False):
    """Install default ssh configs."""
    log.info('Installing .ssh')
    config_dir = Path('~').joinpath('.ssh').expanduser()
    target_configs = script.parent.joinpath('ssh')
    _link_files(config_dir, target_configs, dry_run=dry_run)


def _install_oh_my_zsh(script, dry_run=False):
    log.info("Installing oh-my-zsh")
    zsh_path = Path('~/.oh-my-zsh').expanduser()
    if zsh_path.exists():
        log.debug("oh-my-zsh is already installed")
    elif not dry_run:
        cmd = 'git clone https://github.com/robbyrussell/oh-my-zsh.git "$HOME/.oh-my-zsh"'
        subprocess.run(cmd, shell=True, check=True)

    zsh_custom_path = zsh_path.joinpath('custom')
    target_configs = script.parent.joinpath('zsh_custom')
    _link_files(zsh_custom_path, target_configs, dry_run=dry_run)


def _fetch_submodules(script: Path, dry_run: bool = False) -> None:
    log.info('initializing submodules')
    if dry_run:
        log.debug('git submodule init')
        log.debug('git submodule update')
    else:
        cwd = str(script.parent.resolve())
        subprocess.run('git submodule init', shell=True, check=True, cwd=cwd)
        subprocess.run('git submodule update', shell=True, check=True, cwd=cwd)


def main() -> None:
    """Install the dotfiles and initialize submodules."""
    script_path = Path(sys.argv[0])
    script = script_path.resolve()

    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", default=False)
    parser.add_argument('--verbose', '-v', action='count', default=0)
    args = parser.parse_args()

    # init logging first
    if args.verbose == 1:
        log.setLevel(logging.INFO)
    elif args.verbose > 1:
        log.setLevel(logging.DEBUG)

    if args.dry_run:
        log.setLevel(logging.DEBUG)

    log.debug('starting')
    _fetch_submodules(script, dry_run=args.dry_run)
    _install_dotfiles(script, dry_run=args.dry_run)
    _install_oh_my_zsh(script, dry_run=args.dry_run)
    _install_configs(script, dry_run=args.dry_run)
    _install_ssh_config(script, dry_run=args.dry_run)
    print(maybe_colored('work complete', 'green'))


if __name__ == '__main__':
    main()
