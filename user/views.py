from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse




def new(request):
    return render(request,'new.html')



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
@login_required
def user_dashboard(request):
    return render(request, 'user_dashboard.html')



from django.db.models import Q
from recruiter.models import JobPost, RecruiterProfile
def job_listings(request):
    jobs = JobPost.objects.all()

    title_or_company = request.GET.get('job_title_or_company_name')
    location = request.GET.get('location')
    job_type = request.GET.get('job_type')

    # Filter by job title or company name
    if title_or_company:
        jobs = jobs.filter(
            Q(title__icontains=title_or_company) |  # Filter by job title
            Q(recruiter__recruiterprofile__company_name__icontains=title_or_company)  # Filter by company name through the recruiter profile
        )
    
    # Filter by location
    if location:
        jobs = jobs.filter(location__icontains=location)
    
    # Filter by job type (you will need to make sure job_type is being used correctly in the model)
    if job_type:
        jobs = jobs.filter(job_type=job_type)

    return render(request, 'job_listings.html', {'jobs': jobs})

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')



def login_view(request):
    if request.method == 'POST':  # <-- Must be uppercase 'POST'
        username = request.POST.get('username')  # <-- request.POST (not request.post)
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_dashboard')  # Replace 'home' with your actual URL name
        else:
            return render(request, 'user/userlog.html', {'error': 'Invalid credentials'})
    
    return render(request, 'user/userlog.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        
        user = User.objects.create_user(username=username,password=password,email=email)
        login(request,user)
        return redirect('user_dashboard')
    return render(request,'user/signup.html')

# def profile_view(request):
#     return render(request,'profile.html')

def logout_view(request):
    logout(request)
    return redirect('first')




from django.shortcuts import render, redirect
from .models import userdetails
from .forms import UserProfileForm

def user_profile(request):
    try:
        profile = userdetails.objects.get(Email=request.user.email)
    except userdetails.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            # 🟢 Reload updated data before re-rendering
            return redirect('user_profile')  # Keeps things clean
    else:
        form = UserProfileForm(instance=profile)

    # Make sure to send the current profile for display (profile picture, resume)
    return render(request, 'user/profile.html', {
        'form': form,
        'userdetails': profile
    })





from .forms import UserProfileForm
from .models import userdetails

@login_required
def user_profile(request):
    try:
        user_profile = userdetails.objects.get(Email=request.user.email)  # Fetch userdetails by email
    except userdetails.DoesNotExist:
        # If no profile is found, create a default one or redirect to a profile creation page
        user_profile = userdetails(Email=request.user.email)

    # Handling POST request (form submission)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')  # Redirect back to profile after saving the form
    else:
        form = UserProfileForm(instance=user_profile)  # Pre-fill form with existing user profile data

    return render(request, 'user/profile.html', {
        'form': form,
        'userdetails': user_profile
    })






from recruiter.models import JobPost, JobApplication
from user.models import userdetails

@login_required
def applied_jobs(request):
    try:
        user_profile = userdetails.objects.get(Email=request.user.email)
    except userdetails.DoesNotExist:
        return render(request, 'user/applied_jobs.html', {'applications': []})  # Show empty list if profile doesn't exist

    applications = JobApplication.objects.filter(user=user_profile)
    return render(request, 'user/applied_jobs.html', {'applications': applications})




@login_required
def apply_job(request, job_id):
    job = JobPost.objects.get(id=job_id)

    try:
        user_profile = userdetails.objects.get(Email=request.user.email)
    except userdetails.DoesNotExist:
        return HttpResponse("Please complete your profile before applying to jobs.", status=403)

    # Prevent duplicate applications
    if not JobApplication.objects.filter(user=user_profile, job=job).exists():
        JobApplication.objects.create(
            user=user_profile,
            job=job,
            status='Pending'
        )

    return redirect('applied_jobs')





from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def create_userdetails(sender, instance, created, **kwargs):
    if created:
        userdetails.objects.create(
            Name=instance.username,
            Email=instance.email,
            Address="",
        )



from django.shortcuts import render, redirect
from .forms import MessageForm
from recruiter.models import RecruiterProfile, RecruiterMessage
from django.contrib.auth.models import User

def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['recruiter_email']
            subject = form.cleaned_data['subject']
            msg = form.cleaned_data['message']

            try:
                recruiter_user = User.objects.get(email=email)
                RecruiterMessage.objects.create(
                    recruiter=recruiter_user,
                    sender_name=request.user.username,
                    subject=subject,
                    message=msg
                )
                return redirect('user_dashboard')  # or a success page
            except User.DoesNotExist:
                form.add_error('recruiter_email', 'Recruiter not found with this email.')
    else:
        form = MessageForm()

    return render(request, 'user/send_message.html', {'form': form})




















