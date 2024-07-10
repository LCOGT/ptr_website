from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import permissions, authentication
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializers import UserSerializer
from user.models import StepProgress, CourseEnrollment
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
        errormsg = ''
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect(next)
            else:
                errormsg = 'Username and/or password are incorrect.'
            
        return render(request, self.template_name, context={'form': form, 'message': errormsg})


class UserProfileApi(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

def user_progress_summary(request):
    return render(request, 'user/admin_progress_summary.html', context={'courses': CourseEnrollment.objects.all()})

def user_progress(request, user_id):
    progress = []
    u = User.objects.get(pk=user_id)
    for course in u.courseenrollment_set.all():
        data = {
            'course': course.course.title,
            'lessons': []
        }
        lessonids = [l['lesson__id'] for l in course.course.course_plan.values('lesson__id')]
        for lesson in u.lessonprogress_set.filter(lesson__in=lessonids):
            stepids = [ l['step'] for l in lesson.lesson.lesson_plan.values('step')]
            steps = StepProgress.objects.filter(user=u, step__in=stepids)
            lessondata = {
                'lesson': lesson,
                'steps': steps
            }
            data['lessons'].append(lessondata)
        progress.append(data)
    title = f"User Progress: {u.username} ({u.first_name} {u.last_name})"
    return render(request, 'user/admin_user_progress.html', context={'courses': progress, 'user': u, 'title': title})

