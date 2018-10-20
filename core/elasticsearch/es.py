import click
from elasticsearch import Elasticsearch
from flask import g
from flask.cli import with_appcontext


def get_es():
    if 'es' not in g:
        g.es = Elasticsearch()
    return g.es


def close_es(e=None):
    es = g.pop("es", None)
    if es is not None:
        # es.close()
        pass


def update_es():
    es = get_es()
    # create_index()


@click.command('update-es')
@with_appcontext
def update_es_command():
    """Update Index Data"""
    update_es()
    click.echo('Updated Index')
