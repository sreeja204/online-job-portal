# models.py
from django.db import models

class userdetails(models.Model):
    
    
    Name = models.CharField(max_length=100)
    Phone_number = models.CharField(max_length=10, blank=True, null=True)
    Email = models.EmailField(unique=True)
    Address = models.TextField(max_length=200)
    profile_picture = models.ImageField(
        upload_to='profile_pics/', blank=True, null=True, default='profile_pics/default.jpg'
    )
   
    work_experience = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    languages = models.TextField(blank=True, null=True)
    job_preference = models.CharField(
        max_length=100,
        choices=[
            ('Full-time', 'Full-time'),
            ('Part-time', 'Part-time'),
            ('Internship', 'Internship'),
            ('Freelance', 'Freelance'),
        ],
        blank=True,
        null=True
    )
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return self.Name






