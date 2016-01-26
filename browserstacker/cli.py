# coding: utf-8
import click

from .screenshots import ScreenShotsAPI


@click.group()
def cli():
    pass


@cli.command()
@click.option('--user', default=None, help='Username on BrowserStack.')
@click.option('--key', default=None, help='Access key.')
def list_browsers(user, key):
    click.echo(ScreenShotsAPI(user, key).list_browsers())
