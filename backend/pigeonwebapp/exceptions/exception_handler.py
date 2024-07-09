from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler

from pigeonwebapp.serializers.utils import APIExceptionSerializer

"""
Django exception handler
"""


def custom_exception_handler(exc, context):
    """
    Custom exception handler
    Add code to this method to allow custom exceptions
    If no custom exception is created, returns the basic one
    """
    response = exception_handler(exc, context)

    if isinstance(exc, APIException):
        serializer = APIExceptionSerializer({
            'status': exc.status_code,
            'message': exc.detail,
            'url': context['request'].build_absolute_uri()
        })

        return JsonResponse(data=serializer.data, status=exc.status_code)

    return response