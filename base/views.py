import json
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Job_details, User_Details
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import logout,login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView,FormView,CreateView
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm,CreateJobForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render



class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = CustomUserCreationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('listings')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            User_Details.objects.create(
                user=user,
                full_name=form.cleaned_data.get('full_name', ''),
                self_des=form.cleaned_data.get('self_des', ''),
                email=form.cleaned_data.get('email', ''),
                address=form.cleaned_data.get('address', ''),
                skills=form.cleaned_data.get('skills', ''),
                photo=self.request.FILES.get('photo'),
                resume=self.request.FILES.get('resume'),  # Add this line for resume
                user_type=form.cleaned_data.get('user_type', 'employee'),
                linkedin_page=form.cleaned_data.get('linkedin_page', 'https://in.linkedin.com/'),
                called_as=form.cleaned_data.get('called_as', '')
            )
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
    

class CustomLoginView(LoginView):
    template_name='base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('listings')

from django.shortcuts import get_object_or_404

class OpeningList(LoginRequiredMixin, ListView):
    model = Job_details
    context_object_name = "opening"
    template_name = 'your_template.html'  # Ensure this matches your template path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_details = get_object_or_404(User_Details, user=self.request.user)
        context['user_details'] = user_details
        
        # If user is an employer, filter job listings created by them
        if user_details.user_type == 'employer':
            context['employer_jobs'] = Job_details.objects.filter(user=self.request.user)
        return context

class OpeningListDetails(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = Job_details
    context_object_name = "opening"
    template_name = 'base/job_details_detail.html'  # Ensure this matches your template path
    success_message = "You have successfully applied for this job."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Split requirements and perks into lists
        requirements_text = self.object.requirements
        requirements_list = requirements_text.split(',') if requirements_text else []

        perks_text = self.object.perks
        perks_list = perks_text.split(',') if perks_text else []

        context['requirements_list'] = requirements_list
        context['perks_list'] = perks_list

        # Get user details
        user_details = get_object_or_404(User_Details, user=self.request.user)
        context['user_details'] = user_details

        return context

    def post(self, request, *args, **kwargs):
        job = self.get_object()
        user = request.user

        if job.applicants is None:
            job.applicants = ''

        if user.username not in job.applicants.split(','):
            if job.applicants:
                job.applicants += f',{user.username}'
            else:
                job.applicants = user.username

            job.save()
            messages.success(self.request, self.success_message)

        return redirect('listings-details', pk=job.pk)


class ViewApplicants(LoginRequiredMixin, DetailView):
    model = Job_details
    template_name = 'base/view_applicants.html'  # Ensure this matches your template path
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = self.get_object()

        # Split applicants string into a list
        if job.applicants:
            context['applicants_list'] = job.applicants.split(',')
        else:
            context['applicants_list'] = []

        return context


class UserDetailsView(LoginRequiredMixin, DetailView):
    model = User_Details
    template_name = 'base/user_details.html'
    context_object_name = 'user_details'

    def get_object(self, queryset=None):
        return get_object_or_404(User_Details, user=self.request.user)


class ApplicantDetailsView(LoginRequiredMixin, DetailView):
    model = User_Details
    template_name = 'base/applicant_details.html'
    context_object_name = 'applicant_details'

    def get_object(self, queryset=None):
        username = self.kwargs['username']
        return get_object_or_404(User_Details, user__username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get user details
        user_details = self.get_object()

        # Split skills into a list
        skills_text = user_details.skills
        skills_list = skills_text.split(',') if skills_text else []

        context['skills_list'] = skills_list
        context['applicant_details'] = user_details

        return context

  
class UserDetailsUpdate(UpdateView):
    model = User_Details
    fields = ['self_des', 'email', 'address', 'skills', 'photo','linkedin_page','called_as','full_name']  # Specify fields you want to edit
    template_name = "base/user_details_edit.html"
    success_url = reverse_lazy('listings')

    def get_object(self, queryset=None):
        return get_object_or_404(User_Details, user=self.request.user)  # Get the User_Details instance for the logged-in user

    def form_valid(self, form):
        # Automatically set the user field to the logged-in user
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class CreateJobPosting(LoginRequiredMixin, CreateView):
    model = Job_details
    form_class = CreateJobForm  # Use the custom form
    template_name = 'base/create_job.html'
    success_url = reverse_lazy('listings')

    def form_valid(self, form):
        form.instance.user = self.request.user  # Set the user to the logged-in user
        return super().form_valid(form)


def delete_job(request, pk):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            job_id = data.get('job_id')
            if str(pk) != str(job_id):
                return JsonResponse({'success': False, 'message': 'Invalid job ID.'}, status=400)

            job = get_object_or_404(Job_details, pk=pk)
            job.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# The @csrf_exempt decorator tells Django to ignore CSRF (Cross-Site Request Forgery) protection for this view.
# This is useful for API views or when you're handling POST requests from external sources. 
# Note: In a production environment, it's important to handle CSRF protection properly.
@csrf_exempt
def delete_applicant(request, pk):
    # This function is responsible for deleting an applicant from a job posting.

    # Check if the HTTP request method is POST.
    # POST is used for sending data to the server, like form submissions.
    if request.method == 'POST':
        # Retrieve the job object from the database using the job's primary key (pk).
        # get_object_or_404 tries to get the object and returns a 404 error if the object does not exist.
        job = get_object_or_404(Job_details, pk=pk)

        # Get the username of the applicant to delete from the POST request's data.
        # request.POST.get('applicant') fetches the value associated with the 'applicant' key.
        applicant = request.POST.get('applicant')

        # Check if the job has any applicants.
        if job.applicants:
            # Split the string of applicants into a list. 
            # This list contains each applicant's username.
            applicants_list = [app for app in job.applicants.split(',') if app != applicant]
            
            # Join the list back into a string, separated by commas.
            # This updated string excludes the applicant we want to delete.
            job.applicants = ','.join(applicants_list)
            
            # Save the updated job object back to the database.
            job.save()

        # Redirect the user to the page showing the list of applicants for this job.
        # 'view-applicants' is the name of the URL pattern, and job.pk is the job's primary key.
        return redirect('view-applicants', pk=job.pk)

    # If the request method is not POST, return a JSON response indicating failure.
    # This response includes a message saying that the request method is invalid.
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)


def about(request):
    return render(request, 'base/about.html')