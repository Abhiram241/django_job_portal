from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    OpeningList, OpeningListDetails, CustomLoginView, CustomLogoutView, 
    UserDetailsView, UserDetailsUpdate, RegisterPage, CreateJobPosting, 
    delete_job, ViewApplicants,delete_applicant,ApplicantDetailsView,about
)

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('', OpeningList.as_view(), name='listings'),
    path('job_details/<int:pk>/', OpeningListDetails.as_view(), name='listings-details'),
    path('job_details/<int:pk>/apply/', OpeningListDetails.as_view(), name='apply-now'),
    path('job_details/<int:pk>/applicants/', ViewApplicants.as_view(), name='view-applicants'),
    path('user_details/', UserDetailsView.as_view(), name='user_details'),
    path('create_job/', CreateJobPosting.as_view(), name='create_job'),
    path('user_update/<int:pk>/', UserDetailsUpdate.as_view(), name='user_update'),
    path('delete_job/<int:pk>/', delete_job, name='delete_job'),
    path('job_details/<int:pk>/delete_applicant/', delete_applicant, name='delete-applicant'),
    path('applicant/<str:username>/', ApplicantDetailsView.as_view(), name='applicant-details'),
    path('about/', about, name='about'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
