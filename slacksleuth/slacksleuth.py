import json
import os
import subprocess
import time
import click
from slackclient import SlackClient
from AppKit import NSWorkspace
from plumbum.cmd import imagesnap  # brew install imagesnap


class SlackSleuth(object):
    def __init__(self, token='', channel='', config_file='~/.slacksleuth'):
        self.token = token
        self.channel = channel
        self.config_file = os.path.expanduser(config_file)
        if not self.token and not self.channel:
            try:
                self.load_config()
            except FileNotFoundError:
                click.echo('Please run `slacksleuth setup` to configure.')
                raise click.Abort()
        self.client = SlackClient(self.token)

    def active_app(self):
        return NSWorkspace.sharedWorkspace() \
            .activeApplication()['NSApplicationName']

    def setup(self):
        self.token = click.prompt('Slack API Token:')
        self.channel = click.prompt('Slack Channel:')

    def save_config(self):
        with open(self.config_file, 'w') as config_file:
            json.dump({
                'token': self.token,
                'channel': self.channel,
            }, config_file)

    def load_config(self):
        with open(self.config_file, 'r') as config_file:
            config = json.load(config_file)
            self.token = config.get('token', '')
            self.channel = config.get('channel', '')
            assert self.token, 'Slack API token is not set.'
            assert self.channel, 'Slack channel is not set.'

    def arm(self):
        click.echo('Ready')
        while True:
            try:
                if self.active_app() == 'Slack':
                    filename = os.path.expanduser(f'~/Pictures/slacksleuth-trapped-{time.time()}.jpg')
                    self.trap(filename)
                    time.sleep(0.2)
                    self.expose(filename)
                    time.sleep(2)
                    self.demoralize()
                    click.echo('A potential troll was handled.')
                    break
                time.sleep(0.2)
            except KeyboardInterrupt:
                break
        click.echo('Disarmed.')

    def trap(self, filename):
        imagesnap['-w', '0.5', filename]()

    def expose(self, filename):
        with open(filename, 'rb') as file_content:
            self.client.api_call(
                "files.upload",
                channels=self.channel,
                file=file_content,
                title=f"Troll alert at {time.time()}!"
            )

    def demoralize(self):
        subprocess.call(["/System/Library/CoreServices/Menu Extras/"
                         "User.menu/Contents/Resources/CGSession", "-suspend"])
