import os.path
import shutil

import click
from jinja2 import Environment
env = Environment()


def expand_placeholders(root, path, name):
    p = os.path.join(root, path)
    with open(p) as f:
        source = f.read()
    templ = env.from_string(source)
    with open(p, 'w') as f:
        f.write(templ.render({'name': name}))


@click.group()
def cli():
    pass

@click.command()
@click.argument('name')
def init(name):
    #   copy sample project
    click.echo('init called')
    here = os.path.split(__file__)[0]
    src = os.path.join(here,'_template')
    shutil.copytree(src,name) 

    #   expand templates
    to_be_expanded = [
        'setup.py',
        '_xyz/__init__.py'
    ]
    for templ in to_be_expanded:
        expand_placeholders(name, templ, name)

    #   rename files and folders
    shutil.move(
        os.path.join(name, '_xyz'),
        os.path.join(name, name)
    )
    shutil.move(
        os.path.join(name, '_xyz.egg-info'),
        os.path.join(name, '{}.egg-info'.format(name))
    )


    click.echo('done.')

@click.command()
def serve():
    click.echo('serve called')

cli.add_command(init)
cli.add_command(serve)

def main():
    cli()

