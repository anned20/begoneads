import requests
import re
from tqdm import tqdm


class Collector(object):
    """A class that collects the remote hosts files

    Attributes:
        sources: list
    """

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

    def try_get_sources(self, sources):
        filtered = []

        for source in tqdm(sources):
            response = requests.get(source)

            if response.status_code >= 200 and response.status_code < 300:
                content = str(response.text)

                filtered.append(content)

        return filtered

    def fix_ips(self, sources):
        pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',
                             re.MULTILINE)
        sources = re.sub(pattern, '0.0.0.0', sources)

        return sources

    def filter_hosts(self, hosts):
        hosts = hosts.split('\n')
        hosts = list(set(hosts))

        hosts = [line for line in hosts
                 if line.strip() != '' and not line.startswith('#')]
        hosts = '\n'.join(hosts)

        return hosts

    def get_result(self):
        sources = self.try_get_sources(self.sources)
        sources = '\n'.join(sources)
        hosts = self.fix_ips(sources)
        hosts = self.filter_hosts(hosts)

        return hosts
