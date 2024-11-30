from django.urls import path
from .views import enrolledStudentsUsingAjax

urlpatterns = [
    path('CourseEnrolledListUsingAjax/', enrolledStudentsUsingAjax),
]
