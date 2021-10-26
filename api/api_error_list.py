"""
Ошибки апи должны соответствовать виду json: {"errors": [{"code": Int,
"message": String]}, где code - сквозной номер ошибки по всем апи, message - описание ошибки
"""
code_list = {
    1: 'Template error, token is lost',    # ошибка поиска токена в headers
    2: 'Unknown token',                 # не авторизован на сервере
    3: 'Error analyze refresh token',

    400: 'Bad request',
    401: 'Unauthorized',
    402: 'Payment required',
    403: 'Forbidden',
    404: 'Not found',
    405: 'Method not allowed'
}


def response_api_error(code):
    messages = code_list[code]
    return [{"code": code, "message": messages}]
