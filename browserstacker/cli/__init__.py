# coding: utf-8
import click

from .helpers import APIWrapper, format_browsers


@click.group(context_settings={'auto_envvar_prefix': 'BROWSERSTACK'})
@click.option('-u', '--user', default=None, help='Username on BrowserStack')
@click.option('-k', '--key', default=None, help='Access key')
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
@click.option('-b', '--browser', default=None, help='Browser name')
@click.option('-bv', '--browser-version', default=None, help='Browser version')
@click.option('-o', '--os', default=None, help='OS name')
@click.option('-ov', '--os-version', default=None, help='OS version')
@click.option('-d', '--device', default=None, help='Device name')
def list_browsers(api, browser, browser_version, os, os_version, device):
    click.echo('Available browsers:')
    browsers = api.list_browsers(
        browser=browser, browser_version=browser_version, device=device, os=os, os_version=os_version
    )
    click.echo(format_browsers(browsers))
    click.echo('Total browsers: %s' % len(browsers))


@browserstacker_command
@click.argument('url', required=True)
def make_screenshots(api, url):
    click.echo(api.make_screenshots(url))


@browserstacker_command
@click.argument('job_id', required=True)
def list_screenshots(api, job_id):
    click.echo(api.list_screenshots(job_id))


@browserstacker_command
@click.argument('job_id', required=True)
@click.option('-d', '--destination', default=None, help='Directory to save the images')
def download_screenshots(api, job_id, destination):
    click.echo(api.download_screenshots(job_id, destination))


@browserstacker_command
@click.argument('image_url', required=True)
@click.option('-d', '--destination', default=None, help='Directory to save the image')
def save_screenshot(api, image_url, destination):
    click.echo(api.save_screenshot(image_url, destination))
