import base64
import hashlib

from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User 
from django.http import HttpResponse

from .forms import *
from .utils import *

def user_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        else:
            message = 'Your login credential is incorrect! Please try again.'
            return render(request, 'login.html', {
                'message': message,
            })


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login') 


@csrf_exempt
def reset_password(request):
    to_email = request.POST['email']
    user = User.objects.filter(email=to_email).first()
    if not user:
        return HttpResponse('There is no such user!<br>Please check your email again.')
    
    from_email = "support@bnchmrk.com"
    subject = "Reset Password"
    # path = 'signup.html'
    # temp = codecs.open(path, encoding='utf-8')
    # content = temp.read().replace('[USERNAME]', 'Jason')
    passwd = User.objects.make_random_password()
    user.set_password(passwd)
    user.save()

    content = 'This is the new password: <b>{}</b><br><br>You can login the system with it and change the password again.'.format(passwd)
    response = send_email(from_email, subject, to_email, content)
    return HttpResponse(str(response.status_code))


@login_required(login_url='/login')
def change_password(request):
    msg = ''
    if request.method == 'GET':
        form = ChangePasswordForm()
    else:
        form = ChangePasswordForm(request.POST)
        if form.is_valid():            
            request.user.set_password(form.cleaned_data['new'])
            request.user.save()
            msg = 'Password changed successfully! Please login again.'

    return render(request, 'change_password.html', { 'form': form, 'msg': msg })
