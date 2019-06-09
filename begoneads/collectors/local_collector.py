import requests
import re
from tqdm import tqdm
from begoneads.collectors.base_collector import BaseCollector


class LocalCollector(BaseCollector):
    """A class that collects local host files

    Attributes:
        sources: list
    """

    def try_get_sources(self, sources):
        """Try and get each file"""

        filtered = []

        for source in tqdm(sources):
            with open(source) as _file:
                filtered.append(_file.read())

        return filtered
