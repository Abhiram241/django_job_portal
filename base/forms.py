from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import User_Details,Job_details

class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter your full name'}))
    self_des = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Describe yourself'}), required=True)
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter your address'}), required=True)
    skills = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter your skills (Comma Separated)'}), required=True)
    photo = forms.ImageField(required=True)
    resume = forms.FileField(required=True)  # Add the resume field
    user_type = forms.ChoiceField(choices=User_Details.USER_TYPE_CHOICES, initial='employee', required=True)
    linkedin_page = forms.URLField(initial='https://in.linkedin.com/', required=True, widget=forms.URLInput(attrs={'placeholder': 'Enter your LinkedIn URL'}))
    called_as = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter what you are called as'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

class CreateJobForm(forms.ModelForm):
    class Meta:
        model = Job_details
        fields = ['title', 'description', 'duration', 'salary', 'location', 'company', 'about_the_role', 'requirements', 'perks', 'about_the_company', 'job_type']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter job title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe the job'}),
            'duration': forms.TextInput(attrs={'placeholder': 'Specify the duration'}),
            'salary': forms.TextInput(attrs={'placeholder': 'Enter salary'}),
            'location': forms.TextInput(attrs={'placeholder': 'Enter job location'}),
            'company': forms.TextInput(attrs={'placeholder': 'Enter company name'}),
            'about_the_role': forms.Textarea(attrs={'placeholder': 'Details about the role'}),
            'requirements': forms.Textarea(attrs={'placeholder': 'List job requirements(Comma Separated)'}),
            'perks': forms.Textarea(attrs={'placeholder': 'Describe the perks(Comma Separated)'}),
            'about_the_company': forms.Textarea(attrs={'placeholder': 'Information about the company'}),
            'job_type': forms.Select(attrs={'placeholder': 'Select job type'}),
        }
