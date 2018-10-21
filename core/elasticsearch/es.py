import click
from elasticsearch import Elasticsearch
from flask import g
from flask.cli import with_appcontext
from config import index


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
    import sync
    # create_index()


@click.command('update-es')
@with_appcontext
def update_es_command():
    """Update Index Data"""
    update_es()
    click.echo('Updated Index')


@click.command('create-index')
@with_appcontext
def create_index_command():
    """Create elastic indices"""
    from json import load
    mapping = load(open("tumblr_mappings.json"))
    es = get_es()
    click.echo('Creating Index')
    response = es.indices.create(index=index + "d", body=mapping)
    print(response)
    click.echo('Created Index')
