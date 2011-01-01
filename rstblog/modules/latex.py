# -*- coding: utf-8 -*-
"""
    rstblog.modules.latex
    ~~~~~~~~~~~~~~~~~~~~~

    Simple latex support for formulas.

    :copyright: (c) 2010 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
import os
import re
import tempfile
import shutil
from hashlib import sha1
from os import path, getcwd, chdir
from subprocess import Popen, PIPE
from werkzeug import escape

from docutils import nodes
from docutils.parsers.rst import Directive, directives


DOC_WRAPPER = r'''
\documentclass[12pt]{article}
\usepackage[utf8x]{inputenc}
\usepackage{amsmath}
\usepackage{amsthm}
\usepackage{amssymb}
\usepackage{amsfonts}
\usepackage{mathpazo}
\usepackage{bm}
\pagestyle{empty}
\begin{document}
%s
\end{document}
'''


def wrap_displaymath(math):
    ret = []
    for part in math.split('\n\n'):
        ret.append('\\begin{split}%s\\end{split}\\notag' % part)
    return '\\begin{gather}\n' + '\\\\'.join(ret) + '\n\\end{gather}'


def render_math(context, math):
    relname = '_math/%s.png' % sha1(math.encode('utf-8')).hexdigest()
    full_filename = context.builder.get_full_static_filename(relname)
    url = context.builder.get_static_url(relname)
    if os.path.isfile(full_filename):
        return url

    latex = DOC_WRAPPER % wrap_displaymath(math)

    tempdir = tempfile.mkdtemp()
    try:
        tf = open(path.join(tempdir, 'math.tex'), 'w')
        tf.write(latex.encode('utf-8'))
        tf.close()

        # build latex command; old versions of latex don't have the
        # --output-directory option, so we have to manually chdir to the
        # temp dir to run it.
        ltx_args = ['latex', '--interaction=nonstopmode', 'math.tex']

        curdir = getcwd()
        chdir(tempdir)

        try:
            p = Popen(ltx_args, stdout=PIPE, stderr=PIPE)
            stdout, stderr = p.communicate()
        finally:
            chdir(curdir)

        if p.returncode != 0:
            raise Exception('latex exited with error:\n[stderr]\n%s\n'
                            '[stdout]\n%s' % (stderr, stdout))

        directory = os.path.dirname(full_filename)
        if not os.path.isdir(directory):
            os.makedirs(directory)
        dvipng_args = ['dvipng', '-o', full_filename, '-T', 'tight', '-z9',
                       '-D', str(int(context.builder.config.root_get(
                            'modules.latex.font_size', 16) * 72.27 / 10)),
                       os.path.join(tempdir, 'math.dvi')]
        p = Popen(dvipng_args, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        if p.returncode != 0:
            raise Exception('dvipng exited with error:\n[stderr]\n%s\n'
                            '[stdout]\n%s' % (stderr, stdout))
    finally:
        try:
            shutil.rmtree(tempdir)
        except (IOError, OSError):
            # might happen? unsure
            pass

    return url


class MathDirective(Directive):
    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        'label': directives.unchanged,
        'nowrap': directives.flag
    }

    def run(self):
        latex = '\n'.join(self.content)
        if self.arguments and self.arguments[0]:
            latex = self.arguments[0] + '\n\n' + latex
        url = render_math(self.state.document.settings.rstblog_context, latex)
        return [nodes.raw('', u'<blockquote class="math"><img src="%s" '
                'alt="%s"></blockquote>' % (escape(url), escape(latex)),
                          format='html')]


def setup(builder):
    directives.register_directive('math', MathDirective)
