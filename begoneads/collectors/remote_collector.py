import requests
import re
from tqdm import tqdm
from begoneads.collectors.base_collector import BaseCollector


class RemoteCollector(BaseCollector):
    """A class that collects the remote host files

    Attributes:
        sources: list
    """

    def try_get_sources(self, sources):
        """Try and get each source, don't return them if the request was not succesful"""

        filtered = []

        for source in tqdm(sources):
            response = requests.get(source)

            if response.status_code >= 200 and response.status_code < 300:
                content = str(response.text)

                filtered.append(content)

        return filtered
