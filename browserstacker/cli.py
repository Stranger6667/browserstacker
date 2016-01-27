# coding: utf-8
import click

from .helpers import format_browsers
from .screenshots import ScreenShotsAPI


@click.group()
@click.option('-u', '--user', default=None, help='Username on BrowserStack.')
@click.option('-k', '--key', default=None, help='Access key.')
@click.option('-v', '--verbosity', count=True, help='Verbosity level')
@click.pass_context
def cli(ctx, user, key, verbosity):
    ctx.obj = {'api': ScreenShotsAPI(user, key, verbosity)}


@cli.command()
@click.pass_context
def list_browsers(ctx):
    click.echo('Available browsers:')
    browsers = ctx.obj['api'].list_browsers()
    click.echo(format_browsers(browsers))
    click.echo('Total browsers: %s' % len(browsers))


@cli.command()
@click.option('--job_id', default=None, help='Job ID to list screenshots')
@click.pass_context
def list_screenshots(ctx, job_id):
    click.echo(ctx.obj['api'].list_screenshots(job_id))


@cli.command()
@click.option('--url', default=None, help='Url to make screenshots')
@click.pass_context
def make_screenshots(ctx, url):
    click.echo(ctx.obj['api'].make_screenshots(url))
