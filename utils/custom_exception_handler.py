from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if (
        response is not None
        and response.status_code == 404
        and "detail" in response.data
    ):
        response.data = {"error": "Đối tượng không tồn tại"}
    if (
        response is not None
        and response.status_code == 401
        and "detail" in response.data
    ):
        response.data = {"error": "DATA_INVALID"}

    return response
