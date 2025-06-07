from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.recruiter_login, name='recruiter_login'),
    path('signup/', views.recruiter_signup, name='recruiter_signup'),
    path('dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('profile/', views.recruiter_profile_view, name='recruiter_profile'),
    path('jobpost/', views.post_job, name='post_job'),  # ✅ renamed URL pattern
    path('post-job/', views.post_job, name='post_job'),  # <- This line
    path('applicants/', views.view_applicants, name='view_applicants'),
    path('applications/update/<int:app_id>/', views.update_application_status, name='update_application_status'),
    path('recruiter/posted-jobs/', views.posted_jobs, name='posted_jobs'),
    path('messages/', views.recruiter_messages, name='recruiter_messages'),


]


