import json
import click
import requests
import datetime
import subprocess
import applescript

from time import sleep


def save_config(config):
    with open('slacksleuth.config', 'w') as config_file:
        json.dump(config, config_file)


def load_config():
    try:
        with open('slacksleuth.config', 'r') as config_file:
            return json.load(config_file)
    except:
        response = click.confirm('Unable to load slacksleuth.config, do you want to setup now?')
        if response is True:
            setup_dialog()


def setup_dialog():
    config = {}
    config['slack_token'] = click.prompt('Your slack token (https://api.slack.com/docs/oauth-test-tokens)')
    config['slack_channels'] = click.prompt('Channel where the photo will be posted')
    save_config(config)
    click.echo("""
Saved configuration, you're all set!

Here's how slacksleuth works:
    - Purpose is to track down who is pranking you by posting messages from your slack

    - Once running, it will monitor the title of currently running app
    - If the title contains 'slack' (browser tab title, slack app)
      # This means someone is trying to use your slack
        - take a photo with iSight camera
        - upload to channel of your choice on slack

How to Use:
    - Open Slack app or in browser. Now let it be, we won't touch it ourselves.
    - Open a Finder window and keep it in focus, because we don't want Slack to be the active app right now
    - Open Terminal app and run `slacksleuth arm`
    - Minimize Terminal app, walk away leaving the machine unlocked (bad idea security wise, ALWAYS lock your machine)
    - Wait

How to Disable:
    - Open the minimized Terminal window, hit Ctrl+C to exit the 'armed' mode.
    - Go back to life as usual
    """)


def get_current_application():
    script = applescript.AppleScript('''tell application "System Events"
set frontApp to name of first application process whose frontmost is true
end tell
tell application frontApp
if the (count of windows) is not 0 then
    return name of front window
end if
end tell''')
    return script.run()


def is_slack_current_application():
    current_app = get_current_application()
    if 'slack' in current_app.lower():
        return True
    return False


def take_photo():
    now = datetime.datetime.now()
    filename = '{:%Y%m%d-%H%M}.jpg'.format(now)
    command = 'imagesnap -w 1.0 {0}'.format(filename)
    subprocess.call(command.split())
    return filename


def attack(config):
    filename = take_photo()
    return send_to_slack(config, filename)


def send_to_slack(config, filename):
    token = config['slack_token']
    channels = config['slack_channels']
    files = dict(file=open(filename, 'rb'))
    data = dict(token=token, filetype='jpg', filename=filename, channels=channels)
    r = requests.post('https://slack.com/api/files.upload', files=files, data=data)
    r.raise_for_status()
    response = r.json()
    return response['ok']


def slacksleuth_arm_trap(config):
    try:
        # Main event loop
        while True:
            try:
                if is_slack_current_application():
                    # take a photo, post to slack
                    success = attack(config)
                    if success:
                        # finally, lock screen, so that they can't delete it
                        subprocess.call(["/System/Library/CoreServices/Menu Extras/User.menu/Contents/Resources/CGSession", "-suspend"])
                        break

            except applescript.ScriptError:
                # traceback.print_exc()
                pass
            finally:
                sleep(5)

    except (KeyboardInterrupt):
        pass


# Command Line Interface
@click.group()
def cli():
    pass


@cli.command()
def arm():
    config = load_config()
    slacksleuth_arm_trap(config)


@cli.command()
def setup():
    setup_dialog()

@cli.command()
def test():
    subprocess.call(["/System/Library/CoreServices/Menu Extras/User.menu/Contents/Resources/CGSession", "-suspend"])
