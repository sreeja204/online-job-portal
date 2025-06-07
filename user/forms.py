from django import forms
from .models import userdetails

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = userdetails
        fields = [
            'Name', 'Email', 'Phone_number', 'Address',
            'work_experience', 'education', 'skills',
            'languages', 'job_preference', 'profile_picture', 'resume'
        ]




class MessageForm(forms.Form):
    recruiter_email = forms.EmailField(label='Recruiter Email')
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)
