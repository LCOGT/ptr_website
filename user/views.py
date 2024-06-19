from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.views.generic.edit import UpdateView
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render

from user.models import StepProgress
from user.forms import EnrolForm, LoginForm


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('/')

class Enrol(View):
    form_class = EnrolForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            course, created = form.enrol(request.user)
            if created:
                messages.success(request, f"You have been enrolled on to {course.title}.")
            else:
                messages.warning(request, f"You are already enrolled on to {course.title}.")
            return redirect(course.slug)


class CompleteStep(UpdateView):
    model = StepProgress
    fields = ["complete"]
    template_name_suffix = "_update_form"


class Login(View):
    template_name = 'user/login.html'
    form_class = LoginForm
    
    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})
        
    def post(self, request):
        form = self.form_class(request.POST)
        next = request.GET.get('next', '/')
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect(next)
        message = 'Login failed!'
        return render(request, self.template_name, context={'form': form, 'message': message})
    
def user_progress(request):
    return render(request, 'user/progress.html', context={'steps': StepProgress.objects.filter(user=request.user)})