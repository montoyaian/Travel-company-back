def standard_response(message: str, data=None, http_code=200):
    return {
        "message": message,
        "data": data,
        "http_code": http_code,
    }