# recruiter/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import RecruiterProfile
from .models import JobPost

from django.shortcuts import render
from .models import RecruiterMessage, JobPost  # use your actual Job model
from .models import JobApplication       # adjust if located elsewhere

def recruiter_dashboard(request):
    recruiter = request.user

    jobs_count = JobPost.objects.filter(recruiter=recruiter).count()
    applications_count = JobApplication.objects.filter(job__recruiter=recruiter).count()
    messages_count = RecruiterMessage.objects.filter(recruiter=recruiter).count()

    context = {
        'jobs_count': jobs_count,
        'applications_count': applications_count,
        'messages_count': messages_count,
    }

    return render(request, 'recruiter/recruiter_dashboard.html', context)



from django.shortcuts import render, redirect
from .models import RecruiterProfile
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

def recruiter_profile_view(request):
    profile = RecruiterProfile.objects.get(user=request.user)

    if request.method == 'POST':
        profile.company_name = request.POST.get('company_name')
        profile.industry = request.POST.get('industry')
        profile.location = request.POST.get('location')
        profile.website = request.POST.get('website')
        profile.founded = request.POST.get('founded')
        profile.company_description = request.POST.get('company_description')

        if 'logo' in request.FILES:
            profile.logo = request.FILES['logo']
        
        profile.save()
        messages.success(request, "Profile updated successfully.")

    return render(request, 'recruiter/recruiter_profile.html', {'recruiter': profile})




# from .models import RecruiterProfile
# from django.core.exceptions import ObjectDoesNotExist

# def recruiter_profile(request):
#     try:
#         recruiter = RecruiterProfile.objects.get(user=request.user)
#     except RecruiterProfile.DoesNotExist:
#         recruiter = None  # No profile yet

#     return render(request, 'recruiter/recruiter_profile.html', {'recruiter': recruiter})





def recruiter_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = username
            user.save()

            # Auto login after signup (optional)
            login(request, user)

            messages.success(request, "Account created successfully!")
            return redirect('recruiter_dashboard')

        except IntegrityError:
            messages.error(request, "Email already registered.")

    return render(request, 'recruiter/recruiter_signup.html')
# recruiter/views.py


def recruiter_login(request):
    if request.method == 'POST':
        email = request.POST.get('username')  # Field named 'username' in form, but it's email
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('recruiter_dashboard')
        else:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'recruiter/recruiter_login.html', {'error': 'Invalid email or password.'})

    return render(request, 'recruiter/recruiter_login.html')






@login_required
def post_job(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')
        salary = request.POST.get('salary')

        JobPost.objects.create(
            recruiter=request.user,
            title=title,
            description=description,
            location=location,
            salary=salary
        )
        return redirect('recruiter_dashboard')

    return render(request, 'recruiter/post_job.html')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import JobPost, JobApplication

@login_required
def view_applicants(request):
    recruiter = request.user
    jobs = JobPost.objects.filter(recruiter=recruiter)
    applications = JobApplication.objects.filter(job__in=jobs).select_related('user', 'job')

    return render(request, 'recruiter/view_applicants.html', {
        'applications': applications
    })


from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .models import JobApplication

@require_POST
def update_application_status(request, app_id):
    application = get_object_or_404(JobApplication, id=app_id)
    new_status = request.POST.get('status')
    if new_status in ['Pending', 'Reviewed', 'Shortlisted', 'Rejected']:
        application.status = new_status
        application.save()
    return redirect('applied_users')

@login_required
def posted_jobs(request):
    jobs = JobPost.objects.filter(recruiter=request.user)
    return render(request, 'recruiter/posted_jobs.html', {'jobs': jobs})


from django.shortcuts import render
from .models import RecruiterMessage  # replace with your actual message model

def recruiter_messages(request):
    messages = RecruiterMessage.objects.filter(recruiter=request.user).order_by('-timestamp')
    return render(request, 'recruiter/messages.html', {'messages': messages})



