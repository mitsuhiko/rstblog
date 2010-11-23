# -*- coding: utf-8 -*-
"""
    rstblog.cli
    ~~~~~~~~~~~

    The command line interface

    :copyright: (c) 2010 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
from __future__ import with_statement
import sys
import os
from rstblog.config import Config
from rstblog.builder import Builder


def run(project_folder):
    """Runs the builder for the given project folder."""
    config_filename = os.path.join(project_folder, 'config.yml')
    config = Config()
    if not os.path.isfile(config_filename):
        raise ValueError('root config file is required')
    with open(config_filename) as f:
        config = config.add_from_file(f)
    builder = Builder(project_folder, config)
    builder.run()


def main():
    """Entrypoint for the console script."""
    if len(sys.argv) not in (1, 2):
        print >> sys.stderr, 'usage: rstblog <folder>'
    elif len(sys.argv) == 2:
        folder = sys.argv[1]
    else:
        folder = os.getcwd()
    run(folder)
