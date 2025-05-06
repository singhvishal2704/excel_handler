from rest_framework.response import Response

def success_response(data=None, message="Success", status_code=200):
    return Response({
        "success": True,
        "message": message,
        "data": data
    }, status=status_code)


def error_response(message="An error occurred", status_code=400):
    return Response({
        "success": False,
        "message": message,
        "data": None
    }, status=status_code)