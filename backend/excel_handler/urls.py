from django.urls import path, include

urlpatterns = [
    path('api/', include('excel_handler.api.v1.urls')),
]
