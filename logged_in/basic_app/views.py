from django.shortcuts import render
from basic_app.forms import userForm,userProfileInfoForm
# Create your views here.
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login,logout

def index(request):
    return render(request,'basic_app/index.html')

@login_required
def special(request):
    return HttpResponse('logged in')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
    #return render(request,'basic_app/special.html')

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = userForm(data = request.POST)
        profile_form = userProfileInfoForm(data = request.POST)

        if user_form.is_valid() and profile_form.is_valid():
             user = user_form.save()
             user.set_password(user.password)
             user.save()

             profile = profile_form.save(commit= False)
             profile.user = user

             if 'profile_pic' in request.FILES:
                 profile.profile_pic = request.FILES['profile_pic']

             profile.save()

             registered = True
        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form= userForm()
        profile_form= userProfileInfoForm()

    return render(request,'basic_app/registration.html',{'registered':registered,'user_form':user_form,'profile_form':profile_form})


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("user is not active.")

        else:
            print("someone tried to login")
            print("user : {} and password : {}".format(username,password))
            return HttpResponse('Incorrect details')

    else:
        return render(request,'basic_app/login.html')
