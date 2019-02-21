import requests
import re
from tqdm import tqdm


class Collector(object):
    """A class that collects the remote hosts files

    Attributes:
        sources: list
    """

    def __init__(self, sources):
        self.sources = sources

    def try_get_sources(self, sources):
        """Try and get each source, don't return them if the request was not succesful"""

        filtered = []

        for source in tqdm(sources):
            response = requests.get(source)

            if response.status_code >= 200 and response.status_code < 300:
                content = str(response.text)

                filtered.append(content)

        return filtered

    def fix_ips(self, sources):
        """Replace all IP addresses with 0.0.0.0"""

        pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',
                             re.MULTILINE)
        sources = re.sub(pattern, '0.0.0.0', sources)

        return sources

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
