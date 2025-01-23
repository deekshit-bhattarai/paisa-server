from typing import Any, Dict, Optional, Union
from rest_framework.response import Response
from rest_framework import status as http_status



class CustomResponseMixin:
    """
    Mixin to standardize JSON responses for Django views.
    """

    @staticmethod
    def return_response(
        success: bool,
        message: str,
        data: Optional[Any] = None,
        errors: Optional[Union[Dict, list]] = None,
        status: int = http_status.HTTP_200_OK,
    ) -> Response:
        """
        Return a standardized JSON response.

        :param success: Boolean indicating the success of the operation
        :param message: A short message describing the response
        :param data: The response data (default: None)
        :param errors: Details about errors, if any (default: None)
        :param status: HTTP status code (default: 200)
        :return: JsonResponse object
        """
        response = {
            "success": success,
            "message": message,
            "data": data,
            "errors": errors,
        }
        return Response(response, status=status)
