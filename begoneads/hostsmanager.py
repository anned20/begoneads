import re


start_marker = '### START BeGoneAds ###'
end_marker = '### END BeGoneAds ###'
pattern = re.compile(f'(?<={start_marker})(.*)(?={end_marker})',
                     re.MULTILINE | re.DOTALL)
fullpattern = re.compile(f'(\n\n{start_marker}.*{end_marker})',
                         re.MULTILINE | re.DOTALL)


class HostsManager(object):
    """Manager for the system hosts file"""

    def __init__(self, path):
        self.path = path

        self.get_content()

    def get_content(self):
        """Get current contents of file"""

        file = open(self.path, 'r', encoding='utf-8')
        self.content = file.read()
        file.close()

    def has_begoneads(self):
        """Check if BeGoneAds is installed"""

        return re.search(pattern, self.content)

    def apply_hosts(self, hosts):
        """Apply or append BeGoneAds"""

        if self.has_begoneads():
            self.content = re.sub(pattern, f'\n{hosts}\n', self.content)
        else:
            self.content = f'{self.content}\n\n{start_marker}\n{hosts}\n{end_marker}\n'

    def remove_begoneads(self):
        """Remove BeGoneAds"""

        if self.has_begoneads():
            self.content = re.sub(fullpattern, '', self.content)

    def commit(self):
        """Save hosts file"""

        file = open(self.path, 'w', encoding='utf-8')
        file.write(self.content.replace('\r', ''))
        file.close()
