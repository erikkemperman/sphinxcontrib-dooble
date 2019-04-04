import os
import hashlib
from datetime import datetime

from concurrent.futures import ProcessPoolExecutor, wait
from time import sleep

from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst import Directive
from sphinx.util.osutil import ensuredir

from dooble.idl import Idl
from dooble.dooble import create_marble_from_ast, default_theme
from dooble.render import render_to_file


def get_option(options, key, default):
    if key not in options.keys():
        return default

    return options[key]


class Marble(nodes.General, nodes.Element):
    _pool = ProcessPoolExecutor(max_workers=8)
    _futures = []

    @staticmethod
    def render_marble(text, outfname):
        with open('/home/erik/temp', 'a') as w:
            w.write('render marble ' + text + '\n')
            w.flush()
        idl = Idl()
        ast = idl.parse(text)
        marble = create_marble_from_ast(ast)
        render_to_file(marble, outfname, default_theme)

    @staticmethod
    def wait_marbles(app, exception):
        with open('/home/erik/temp', 'a') as w:
            w.write('waiting marbles %d\n' % len(Marble._futures))
            w.flush()
        sleep(30)
        wait(Marble._futures)


def generate_name(self, node):
    h = hashlib.sha1()
    h.update(node['text'].encode('utf-8'))
    key = h.hexdigest()
    fname = 'marble-{}.png'.format(key)
    imgpath = getattr(self.builder, 'imgpath', None)
    if imgpath:
        return ('/'.join((self.builder.imgpath, fname)),
                os.path.join(self.builder.outdir, '_images', fname))
    else:
        return fname, os.path.join(self.builder.outdir, fname)


def schedule_marble(self, node):
    refname, outfname = generate_name(self, node)
    if not os.path.exists(outfname):
        with open('/home/erik/temp', 'a') as w:
            w.write(str(self) + '\n')
            w.write('go marble %d\n' % len(Marble._futures))
            w.write('  ' + node['text'] + '\n')
            w.flush()
        ensuredir(os.path.dirname(outfname))
        try:
            future = Marble._pool.submit(Marble.render_marble, (node['text'], outfname))
            Marble._futures.append(future)
        except Exception as e:
            with open('/home/erik/temp', 'a') as w:
                w.write(
                    'eek ' + str(e) + '\n')
                w.flush()

    return refname, outfname


def html_visit_marble(self, node):

    refname, outfname = schedule_marble(self, node)
    html_block = '<img src="{}" alt="{}"/>\n'.format(
        self.encode(refname),
        self.encode(node['alt']),
    )

    self.body.append(self.starttag(node, 'p', CLASS='marble'))
    self.body.append(html_block)
    self.body.append('</p>\n')


def html_depart_marble(self, node):
    pass


def latex_visit_marble(self, node):
    refname, outfname = schedule_marble(self, node)
    latex_block = '\\includegraphics{{{}}}\n'.format(
        self.encode(refname)
    )
    self.body.append(latex_block)


def latex_depart_marble(self, node):
    pass


class MarbleDirective(Directive):
    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        'alt': directives.unchanged,
    }

    def run(self):
        alt = get_option(self.options, 'alt', 'marble diagram')

        env = self.state.document.settings.env
        relfn = env.doc2path(env.docname, base=None)
        text = '\n'.join(self.content)

        node = Marble(self.block_text, alt=alt)
        node['text'] = text
        node['filename'] = os.path.split(relfn)[1]
        return [node]


def setup(app):
    app.add_node(Marble,
        html=(html_visit_marble, html_depart_marble),
        latex=(latex_visit_marble, latex_depart_marble)
    )

    app.add_directive('marble', MarbleDirective)
    app.connect('build-finished', Marble.wait_marbles)
    return {'parallel_read_safe': True}
