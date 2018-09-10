#!/usr/bin/env python3
# coding: utf-8
from __future__ import absolute_import

import filecmp
import getopt
import sys
from os import symlink
from pathlib import Path


def short_help():
    """Print the help message and exits."""
    print('install.py [-h] [--dry-run]')
    sys.exit(2)


def long_help():
    short_help()


def link_file(link, target, dry_run=False):
    """Create a symlink at link to target.

    :param link:    the name of the link to create
    :type link:     pathlib.Path
    :param target:  the target that the link points to
    :type target:   pathlib.Path
    """
    target_uri = target.resolve()
    link_uri = link.resolve()
    print("linking file '{}' to '{}'".format(link_uri, target_uri))
    if not dry_run:
        symlink(target_uri, link_uri, target_is_directory=target.is_dir())


def replace_file(link, target, dry_run=False):
    """Replace file at link with a symlink to target.

    :param link:    the name of the link to create
    :type link:     pathlib.Path
    :param target:  the target that the link points to
    :type target:   pathlib.Path
    """
    target_uri = target.resolve()
    link_uri = link.resolve()
    print("replacing file: {}".format(link))
    if not dry_run:
        backup_uri = "{}.bak".format(link_uri)
        link.replace(backup_uri)
        symlink(target_uri, link_uri, target_is_directory=target.is_dir())


def install_gitconfig(dry_run=False):
    """Install the global gitconfig file.

    This file is special because we want some sections to be untracked.
    Use include to handle this case https://git-scm.com/docs/git-config#_includes
    """
    global_config_file = Path('~').joinpath('.gitconfig').expanduser()
    source_config_file = Path('.').joinpath('gitconfig')
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


def install(dry_run=False):
    p = Path('.')
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
    for f in p.iterdir():
        if f.name in to_skip:
            continue
        home_dir_file = Path('~').joinpath(".{}".format(f.name)).expanduser()
        if home_dir_file.exists():
            if f.is_file() and filecmp.cmp(f, home_dir_file):
                print("identical {}".format(home_dir_file))
            elif f.is_dir() and filecmp.dircmp(f, home_dir_file):
                print("identical {}".format(home_dir_file))
            else:
                replace_file(home_dir_file, f, dry_run=dry_run)
        else:
            link_file(home_dir_file, f, dry_run=dry_run)
    install_gitconfig(dry_run=dry_run)


def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'h', ['help', 'dry-run'])
    except getopt.GetoptError:
        short_help()

    dry_run = False
    for opt, arg in opts:
        if opt == '-h':
            short_help()
        elif opt == '--help':
            long_help()
        elif opt == '--dry-run':
            dry_run = True

    install(dry_run=dry_run)


if __name__ == '__main__':
    main(sys.argv[1:])
