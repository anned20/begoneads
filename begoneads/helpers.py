import os


def is_admin(is_windows):
    if is_windows:
        try:
            # only windows users with admin privileges can read the C:\windows\temp
            _ = os.listdir(os.sep.join(
                [os.environ.get('SystemRoot', 'C:\\windows'), 'temp']))

            return True
        except PermissionError:
            return False
    else:
        if os.geteuid() == 0:
            return True
        else:
            return False
