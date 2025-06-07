from django.urls import path
from user import views
urlpatterns = [
    
    path('',views.new,name='first'),
    
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('login/',views.login_view,name='login'),
    path('signup/',views.signup_view,name='signup'),
    path('logout/',views.logout_view,name='logout'),
    path('profile/', views.user_profile, name='user_profile'),  # Profile page URL
    path('jobs/', views.job_listings, name='job_listings'),
    path('apply-job/<int:job_id>/', views.apply_job, name='apply_job'),
    path('applied-jobs/', views.applied_jobs, name='applied_jobs'),
    path('send-message/', views.send_message, name='send_message'),
]


       
   

