class ApiError(Exception):
    pass

class ParamsError(ApiError):
    pass

class IdsError(ApiError):
    pass

class DataError(ApiError):
    pass