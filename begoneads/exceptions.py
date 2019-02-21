class NotElevatedException(Exception):
    pass


class InvalidSourceException(Exception):
    def __init__(self, source):
        self.message = f'{source} is not a valid source'

    def __str__(self):
        return self.message
