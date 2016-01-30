# coding: utf-8
import click

from .helpers import APIWrapper, format_browsers


@click.group()
@click.option('-u', '--user', default=None, help='Username on BrowserStack.')
@click.option('-k', '--key', default=None, help='Access key.')
@click.option('-v', '--verbosity', count=True, help='Verbosity level')
@click.version_option()
@click.pass_context
def cli(ctx, user, key, verbosity):
    ctx.obj = APIWrapper(user, key, verbosity=verbosity)


def browserstacker_command(func):
    """
    Shortcut to define command for BrowserStacker.
    """
    pass_decorator = click.make_pass_decorator(APIWrapper)
    return cli.command()(pass_decorator(func))


@browserstacker_command
def list_browsers(api):
    click.echo('Available browsers:')
    browsers = api.list_browsers()
    click.echo(format_browsers(browsers))
    click.echo('Total browsers: %s' % len(browsers))


@browserstacker_command
@click.argument('job_id', required=True)
def list_screenshots(api, job_id):
    click.echo(api.list_screenshots(job_id))


@browserstacker_command
@click.argument('url', required=True)
def make_screenshots(api, url):
    click.echo(api.make_screenshots(url))
