from django.http import JsonResponse
from django.db.models.deletion import ProtectedError
import logging

logger = logging.getLogger(__name__)


class CustomExceptionHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, ProtectedError):
            # Kiểm tra xem 'protected_objects' có tồn tại hay không
            if hasattr(exception, "protected_objects"):
                protected_instances = exception.protected_objects
                error_message = f"Không thể xóa một số bản ghi của mô hình vì chúng được tham chiếu thông qua các khóa ngoại bảo vệ: {protected_instances}."
                logger.error(error_message)
                return JsonResponse({"error": error_message}, status=400)

            # Nếu không có 'protected_objects', thử lấy tên mô hình từ 'model' attribute
            elif hasattr(exception, "model"):
                model_name = exception.model.__name__
                error_message = f"Không thể xóa một số bản ghi của mô hình '{model_name}' vì chúng được tham chiếu thông qua các khóa ngoại bảo vệ."
                logger.error(error_message)
                return JsonResponse({"error": error_message}, status=400)

        # Trả về None để chuyển giao xử lý lỗi cho middleware tiếp theo
        return None
