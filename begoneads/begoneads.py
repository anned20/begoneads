#!/usr/bin/env python3

import os
import sys
import re
import click
from begoneads.collector import Collector
from begoneads.hostsmanager import HostsManager
from begoneads.exceptions import *
from begoneads.helpers import is_admin

# Default sources
sources = [
    'https://www.malwaredomainlist.com/hostslist/hosts.txt',
    'https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.Dead/hosts',
    'https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.Spam/hosts',
    'https://someonewhocares.org/hosts/zero/hosts',
    'http://winhelp2002.mvps.org/hosts.txt',
    'https://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts&mimetype=plaintext&useip=0.0.0.0',
    'https://raw.githubusercontent.com/mitchellkrogza/Badd-Boyz-Hosts/master/hosts',
    'https://zerodot1.gitlab.io/CoinBlockerLists/hosts_browser',
    'https://raw.githubusercontent.com/FadeMind/hosts.extras/master/UncheckyAds/hosts',
    'https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.2o7Net/hosts',
    'https://raw.githubusercontent.com/azet12/KADhosts/master/KADhosts.txt',
    'https://raw.githubusercontent.com/AdAway/adaway.github.io/master/hosts.txt',
    'https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.Risk/hosts',
]


@click.group()
def cli():
    """Install or uninstall BeGoneAds, the host blocker for the system hosts file"""


@cli.command('install', short_help='Install or update BeGoneAds')
@click.option('--sources', is_flag=False, default=','.join(sources),
              type=click.STRING, help='Sets sources to fetch from, seperated by ,')
def install(sources):
    # Check if we have sufficient permissions
    if not is_admin(sys.platform.startswith('win')):
        raise NotElevatedException(
            'This program needs to be run as root to work properly')

    sources = [i.strip() for i in sources.split(',')]

    url_pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        # domain...
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE
    )

    for source in sources:
        if not re.match(url_pattern, source):
            raise InvalidSourceException(source)

    # Collect hosts for hosts file
    collector = Collector(sources)

    print('⋯ Collecting and parsing hosts')
    hosts = collector.get_result()

    print('✓ Hosts collected')

    if sys.platform.startswith('win'):
        path = r'c:\windows\system32\drivers\etc\hosts'
    else:
        path = '/etc/hosts'

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

    if sys.platform.startswith('win'):
        path = r'c:\windows\system32\drivers\etc\hosts'
    else:
        path = '/etc/hosts'

    print('⋯ Parse current hosts file')
    hosts_manager = HostsManager(path)

    print('⋯ Removing BeGoneAds')
    hosts_manager.remove_begoneads()

    print('⋯ Saving')
    hosts_manager.commit()

    print('✓ BeGoneAds uninstalled')


if __name__ == '__main__':
    cli()
