# coding: utf-8
import click

from .helpers import APIWrapper, format_browsers
from ..constants import ORIENTATIONS, MAC_RESOLUTIONS, WIN_RESOLUTIONS, QUALITIES, LOCALS, WAIT_TIMES


@click.group(context_settings={'auto_envvar_prefix': 'BROWSERSTACK'})
@click.option('-u', '--user', help='Username on BrowserStack')
@click.option('-k', '--key', help='Access key')
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


def browsers_options(func):
    return click.option('-b', '--browser', multiple=True, help='Browser name')(
        click.option('-bv', '--browser-version', multiple=True, help='Browser version')(
        click.option('-os', '--os', multiple=True, help='OS name')(
        click.option('-ov', '--os-version', multiple=True, help='OS version')(
        click.option('-d', '--device', multiple=True, help='Device name')(func)))))


def screenshots_options(func):
    return click.option('-o', '--orientation', type=click.Choice(ORIENTATIONS), help='Screen orientation')(
        click.option('-m', '--mac-res', type=click.Choice(MAC_RESOLUTIONS), help='Screen resolution on OS X')(
        click.option('-w', '--win-res', type=click.Choice(WIN_RESOLUTIONS), help='Screen resolution on Windows')(
        click.option('-q', '--quality', type=click.Choice(QUALITIES), help='Quality of the screenshot')(
        click.option('-l', '--local', type=click.Choice(LOCALS), help='Local testing')(
        click.option('-t', '--wait-time', type=click.Choice(WAIT_TIMES), help='Seconds before taking screenshot')(
        click.option('-c', '--callback-url', help='Results will be send to this URL')(func)))))))


@browserstacker_command
@browsers_options
def browsers(api, **kwargs):
    click.echo('Available browsers:')
    browsers = api.browsers(**kwargs)
    click.echo(format_browsers(browsers))
    click.echo('Total browsers: %s' % len(browsers))


def get_browsers(api, browser, browser_version, os, os_version, device):
    if any([browser, browser_version, os, os_version, device]):
        return api.browsers(browser, browser_version, device, os, os_version)


@browserstacker_command
@click.argument('url', required=True)
@click.option('-ds', '--destination', help='Directory to save the images')
@browsers_options
@screenshots_options
def make(api, url, browser, browser_version, os, os_version, device, **kwargs):
    kwargs['browsers'] = get_browsers(api, browser, browser_version, device, os, os_version)
    click.echo(api.make(url, **kwargs))


@browserstacker_command
@click.argument('url', required=True)
@browsers_options
@screenshots_options
def generate(api, url, browser, browser_version, os, os_version, device, **kwargs):
    kwargs['browsers'] = get_browsers(api, browser, browser_version, device, os, os_version)
    click.echo(api.generate(url, **kwargs))


@browserstacker_command
@click.argument('job_id', required=True)
def list(api, job_id):
    click.echo(api.list(job_id))


@browserstacker_command
@click.argument('job_id', required=True)
@click.option('-ds', '--destination', help='Directory to save the images')
def download(api, job_id, destination):
    click.echo(api.download(job_id, destination))
