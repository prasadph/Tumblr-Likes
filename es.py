import click
from flask import current_app, g
from flask.cli import with_appcontext
from elasticsearch import Elasticsearch


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
