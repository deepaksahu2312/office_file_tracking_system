from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth import authenticate, login
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib import messages
from content.decorators import login_required_message
from .models import *
from .admin import UserCreationForm, StaffCreationForm
import json

def index(request):
    response = {}
    print(request.user, " logged in : RENDER HOME ")
    user = CustomUser.objects.filter(id=request.user.id)
    print("User : ",user)
    if not user or (user and user[0].is_student):
        return render(request, 'student_home.html', response)
    else:
        return render(request, 'staff_home.html', response)

class UserFormView(generic.View):
    form_class = UserCreationForm
    template_name = 'accounts/student_register.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            print(user)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            return redirect('/')

        return render(request, self.template_name, {'form': form})

class StaffFormView(generic.View):
    form_class = StaffCreationForm
    template_name = 'accounts/staff_register.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            print(user)
            user.is_student = False
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            return redirect('/')

        return render(request, self.template_name, {'form': form})

@csrf_exempt
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return HttpResponseRedirect('/login/')

@csrf_exempt
def user_login(request):
    response = {}
    if request.user.is_authenticated:
        logout(request)
    else:
        response = {}
    if request.method == 'POST':
        next_post = request.POST.get('next')
        redirect_path = next_post
        username = request.POST['username']
        try:
            username = CustomUser.objects.get(email=username).username
        except CustomUser.DoesNotExist:
            username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, 'You have been successfully logged in.')
                if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
                    return redirect(redirect_path)
                else:
                    return redirect('accounts:index')
            else:
                messages.warning(request, 'User is not active yet')
                response['message'] = 'User is not active yet'
        else:
            messages.warning(request, 'User is invalid')
            response['message'] = 'User is invalid'

    return render(request, 'accounts/login.html', response)

@csrf_exempt
def getNames(request):
    print("INSIDE GET NAMES")
    if request.method == 'POST':
        designation = request.POST.get('d')
        result_set = []
        trimmed_role= str(designation).strip()
        all_users = CustomUser.objects.filter(role=trimmed_role, is_student=False)
        print('..',trimmed_role,'..')
        for user in all_users:
            print(user.first_name,' ', user.id)
            result_set.append({'first_name': user.first_name,'last_name': user.last_name, 'id': user.id})
        return HttpResponse(json.dumps(result_set), content_type='application/json')

    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

@csrf_exempt
@login_required_message(message="You should be logged in, in order to perform this")
@login_required(login_url="/login/")
def Activate_Users(request):
    users = CustomUser.objects.all()
    response = {}
    response['users'] = users
    return render(request, 'accounts/activate_users.html', response)

@csrf_exempt
@login_required_message(message="You should be logged in, in order to perform this")
@login_required(login_url="/login/")
def Activate(request, uid):
    user = CustomUser.objects.get(pk=uid)
    user.is_active = True
    user.save()
    response = {}
    users = CustomUser.objects.all()
    response['users'] = users
    print("activate")
    return render(request, 'accounts/activate_users.html', response)

@csrf_exempt
@login_required_message(message="You should be logged in, in order to perform this")
@login_required(login_url="/login/")
def Deactivate(request, uid):
    user = CustomUser.objects.get(pk=uid)
    user.is_active = False
    user.save()
    response = {}
    users = CustomUser.objects.all()
    response['users'] = users
    print("deactivate")
    return render(request, 'accounts/activate_users.html', response)