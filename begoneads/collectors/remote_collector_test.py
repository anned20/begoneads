from begoneads.collectors.remote_collector import RemoteCollector
from unittest.mock import patch

collector = RemoteCollector([])


def test_try_get_sources():
    with patch('requests.get') as mock_request:
        url = 'https://somewhere.com/that/has/hosts'

        mock_request.return_value.status_code = 200
        mock_request.return_value.text = 'response'

        assert collector.try_get_sources([url]) == ['response']
        mock_request.assert_called_once_with(url)

    with patch('requests.get') as mock_request:
        url = 'https://somewhere.com/that/has/hosts/but/with/error'

        mock_request.return_value.status_code = 404

        assert collector.try_get_sources([url]) == []
        mock_request.assert_called_once_with(url)


def test_fix_ips():
    before = '127.0.0.1 some.host'

    result = collector.fix_ips(before)

    assert result == '0.0.0.0 some.host'
