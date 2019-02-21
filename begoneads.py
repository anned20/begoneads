import os
import sys
import re
import click
from collector import Collector
from hostsmanager import HostsManager
from exceptions import NotElevatedException
from helpers import is_admin


@click.group()
def cli():
    """Install or uninstall BeGoneAds, the host blocker for the system hosts file"""


@cli.command('install', short_help='Install or update BeGoneAds')
def install():
    # Check if we have sufficient permissions
    if not is_admin(sys.platform.startswith('win')):
        raise NotElevatedException(
            'This program needs to be run as root to work properly')

    # Collect hosts for hosts file
    collector = Collector()

    print('⋯ Collecting and parsing hosts')
    hosts = collector.get_result()

    print('✓ Hosts collected')

    if sys.platform.startswith('win'):
        path = r'c:\windows\system32\drivers\etc\hosts'
    else:
        path = '/etc/hosts'

    # Write to hosts file
    print('⋯ Parse current hosts file')
    hosts_manager = HostsManager(path)

    print('⋯ Applying new hosts')
    hosts_manager.apply_hosts(hosts)

    print('⋯ Saving')
    hosts_manager.commit()

    print('✓ Hosts applied')


@cli.command('uninstall', short_help='Uninstall BeGoneAds')
def uninstall():
    # Check if we have sufficient permissions
    if not is_admin(sys.platform.startswith('win')):
        raise NotElevatedException(
            'This program needs to be run as root to work properly')

    # Write to hosts file
    print('⋯ Parse current hosts file')
    hosts_manager = HostsManager('/etc/hosts')

    print('⋯ Removing BeGoneAds')
    hosts_manager.remove_begoneads()

    print('⋯ Saving')
    hosts_manager.commit()

    print('✓ BeGoneAds uninstalled')


if __name__ == '__main__':
    cli()
