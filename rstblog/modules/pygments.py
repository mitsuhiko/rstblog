# -*- coding: utf-8 -*-
"""
    rstblog.modules.pygments
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Adds support for pygments.

    :copyright: (c) 2010 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import
from rstblog.signals import before_file_processed, \
     before_build_finished

from docutils import nodes
from docutils.parsers.rst import Directive, directives

from pygments import highlight
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.formatters import HtmlFormatter
from pygments.styles import get_style_by_name


html_formatter = None


class CodeBlock(Directive):
    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    lexers_config = {}

    def run(self):
        try:
            lexer = get_lexer_by_name(self.arguments[0])
            self.configure_lexer(lexer)
        except ValueError:
            lexer = TextLexer()
        code = u'\n'.join(self.content)
        formatted = highlight(code, lexer, html_formatter)
        return [nodes.raw('', formatted, format='html')]

    def configure_lexer(self, lexer):
        if lexer.name not in self.lexers_config:
            return

        config = self.lexers_config[lexer.name]
        for kv in config:
            property = kv.keys()[0]
            setattr(lexer, property, kv[property])

def inject_stylesheet(context, **kwargs):
    context.add_stylesheet('_pygments.css')


def write_stylesheet(builder, **kwargs):
    with builder.open_static_file('_pygments.css', 'w') as f:
        f.write(html_formatter.get_style_defs())


def setup(builder):
    global html_formatter

    lexers_config = builder.config.root_get('modules.pygments.lexers', {})
    for config in lexers_config:
        language = config.keys()[0];
        CodeBlock.lexers_config[language] = config[language]

    style = get_style_by_name(builder.config.root_get('modules.pygments.style'))
    html_formatter = HtmlFormatter(style=style)
    directives.register_directive('code-block', CodeBlock)
    directives.register_directive('sourcecode', CodeBlock)
    before_file_processed.connect(inject_stylesheet)
    before_build_finished.connect(write_stylesheet)
