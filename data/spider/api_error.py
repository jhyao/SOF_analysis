class ApiError(Exception):
    pass

class UrlParamsError(ApiError):
    pass

class UrlKeysError(ApiError):
    pass

class DataError(ApiError):
    def __init__(self, error):
        super().__init__(error)
        self.error_id = error.get('error_id', 0)
        self.error_message = error.get('error_message', '')
        self.error_name = error.get('error_name', 'unnamed')


if __name__ == '__main__':
    raise DataError(error_id=502, error_message='sdfsd', error_name='sf')

