import requests
import re
from tqdm import tqdm


class BaseCollector(object):
    """A base class for all collectors

    Attributes:
        sources: list
    """

    def __init__(self, sources):
        self.sources = sources

    def try_get_sources(self, sources):
        """Try and get each file"""

        filtered = []

        for source in tqdm(sources):
            with open(source) as _file:
                filtered.append(_file.read())

        return filtered

    def fix_ips(self, hosts):
        """Replace all IP addresses with 0.0.0.0"""

        hosts = re.sub(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', '0.0.0.0', hosts, 0, re.MULTILINE)

        return hosts

    def filter_hosts(self, hosts):
        """Only keep meaningful lines"""

        hosts = hosts.split('\n')
        hosts = list(set(hosts))

        hosts = [line for line in hosts
                 if line.strip() != '' and not line.startswith('#')]
        hosts = '\n'.join(hosts)

        return hosts

    def get_result(self):
        """Get usable result"""

        sources = self.try_get_sources(self.sources)
        sources = '\n'.join(sources)
        hosts = self.fix_ips(sources)
        hosts = self.filter_hosts(hosts)

        return hosts
