# Generated by Django 5.1.7 on 2025-03-16 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_job'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='category',
            field=models.CharField(choices=[('IT', 'IT'), ('Finance', 'Finance'), ('Marketing', 'Marketing'), ('HR', 'HR'), ('Healthcare', 'Healthcare'), ('Education', 'Education')], max_length=100),
        ),
        migrations.AlterField(
            model_name='job',
            name='location',
            field=models.CharField(choices=[('New York', 'New York'), ('Los Angeles', 'Los Angeles'), ('Chicago', 'Chicago'), ('Houston', 'Houston'), ('San Francisco', 'San Francisco')], max_length=100),
        ),
    ]
