from django.db import models
from django.contrib.auth.models import User

class Job_details(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    duration = models.CharField(max_length=100)
    salary = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    about_the_role = models.TextField()
    requirements = models.TextField()
    perks = models.TextField()
    about_the_company = models.TextField()
    job_type = models.CharField(max_length=50, choices=[
        ('fulltime', 'Full Time'),
        ('halftime', 'Half Time'),
    ], default='fulltime')
    created = models.DateTimeField(auto_now_add=True)
    applicants = models.TextField(null=True, blank=True)  # Field to store applicants' usernames

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['created']



class User_Details(models.Model):
    USER_TYPE_CHOICES = [
        ('employer', 'Employer'),
        ('employee', 'Employee'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name= models.CharField( max_length=100,default='abhiram')
    self_des = models.TextField( default='This is description')
    email = models.EmailField()
    address = models.TextField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=False)  # Field for photo
    resume = models.FileField(upload_to='resumes/', null=True, blank=True, default='resumes/default_resume.pdf')
    user_type = models.CharField(max_length=50, choices=USER_TYPE_CHOICES, default='employee')
    linkedin_page= models.CharField( max_length=100,default='https://www.youtube.com/')
    called_as =  models.CharField(max_length=300, null=True, blank=False,default='This is description')
    def __str__(self):
        return f"{self.user}"
    def get_skills_list(self):
        if self.skills:
            return self.skills.split(',')
        return []

