import click
from .slacksleuth import SlackSleuth


# Command Line Interface
@click.group()
def cli():
    pass


@cli.command()
def arm():
    ss = SlackSleuth()
    ss.arm()


@cli.command()
def setup():
    ss = SlackSleuth()
    ss.setup()
    ss.save_config()
