from django.template import RequestContext
from User.forms import UserForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib import messages


def auth_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)

        else:
            messages.add_message(request, messages.ERROR, 'User not active')
    else:
        messages.add_message(request, messages.ERROR, 'Wrong username or password')
    redirect_to = request.POST.get('next', '')
    return HttpResponseRedirect(redirect_to)


def auth_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index' ,args=('',)))


def index(request, user_id):
    if user_id == u'None':
        user = User()
    else:
        user = User.objects.get(pk=user_id)
    form = UserForm(instance=user)
    return render_to_response('user/index.html', {'form': form, 'user': user}, RequestContext(request))


def save(request, user_id):
    if request.method == 'POST':
        if user_id == u'None':
            form = UserForm(request.POST)
        else:
            user = User.objects.get(pk=user_id)
            form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.instance
            user.set_password(request.POST.get('password'))
            user.save()
            user = authenticate(username=form.instance.username, password=request.POST.get('password'))
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Registration completed welcome '+user.get_full_name())
        return HttpResponseRedirect(reverse('index' ,args=('',)))
    else:
        form = UserForm
    c = {'form': form}
    return render_to_response('user/index.html', c, RequestContext(request))