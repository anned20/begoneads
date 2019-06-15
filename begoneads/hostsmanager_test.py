from begoneads.hostsmanager import HostsManager, start_marker, end_marker
from unittest.mock import patch, mock_open

without_begoneads = '''
127.0.0.1 localhost whatever-hostname
0.0.0.0 some.local
'''

with_begoneads = f'''
127.0.0.1 localhost whatever-hostname
0.0.0.0 some.local

{start_marker}
0.0.0.0 inserted.by.begoneads
{end_marker}
'''


def test_has_begoneads():
    with patch('builtins.open', mock_open(read_data=without_begoneads)) as mock_file:
        hosts_manager = HostsManager('/etc/hosts')
        mock_file.assert_called_with('/etc/hosts', 'r', encoding='utf-8')

        assert hosts_manager.has_begoneads() == None

    with patch('builtins.open', mock_open(read_data=with_begoneads)) as mock_file:
        hosts_manager = HostsManager('/etc/hosts')
        mock_file.assert_called_with('/etc/hosts', 'r', encoding='utf-8')

        assert hosts_manager.has_begoneads()


def test_apply_hosts():
    with patch('builtins.open', mock_open(read_data=without_begoneads)) as mock_file:
        hosts_manager = HostsManager('/etc/hosts')
        mock_file.assert_called_with('/etc/hosts', 'r', encoding='utf-8')

        assert hosts_manager.has_begoneads() == None

        hosts_manager.apply_hosts('0.0.0.0 some.test')

        assert hosts_manager.has_begoneads()


def test_remove_begoneads():
    with patch('builtins.open', mock_open(read_data=with_begoneads)) as mock_file:
        hosts_manager = HostsManager('/etc/hosts')
        mock_file.assert_called_with('/etc/hosts', 'r', encoding='utf-8')

        assert hosts_manager.has_begoneads()

        hosts_manager.remove_begoneads()

        assert hosts_manager.has_begoneads() == None
