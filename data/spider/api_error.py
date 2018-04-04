class ApiError(Exception):
    pass

class UrlParamsError(ApiError):
    pass

class UrlKeysError(ApiError):
    pass

class DataError(ApiError):
    pass