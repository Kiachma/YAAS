from django.template import RequestContext
from django.shortcuts import render
from User.forms import UserForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


def auth_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)

        else:
         a=1
    else:
        a=1
    return HttpResponseRedirect(reverse('auctions:index'))
def auth_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('auctions:index'))

def index(request, user_id):
    if user_id ==u'None':
        user=User()
    else:
        user = User.objects.get(pk=user_id)
    form = UserForm(instance=user)
    return render_to_response('user/index.html' ,{'form': form,'user' : user}, RequestContext(request))



def save(request, user_id):
    if request.method == 'POST':
        if user_id==u'None':
            form=UserForm(request.POST)
        else:
            user = User.objects.get(pk=user_id)
            form = UserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('user:index' ,args=(form.instance.id,)))
    else:
        form = UserForm
    c={'form': form}
    return render_to_response('user/index.html',c , RequestContext(request))