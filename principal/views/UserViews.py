import hashlib

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http.response import HttpResponse, JsonResponse, \
    HttpResponseRedirect
from django.shortcuts import redirect, render_to_response
from django.template.context import RequestContext

from principal.forms import LoginForm, TravellerRegistrationForm
from principal.services import TravellerService
from principal.utils import BrainTravelUtils
from principal.views import EmailViews
from django.utils.translation import ugettext as _


def sign_in(request):
    registerForm = TravellerRegistrationForm()
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user.is_active:
                    login(request, user)
                    return redirect("/")
                else:
                    return render_to_response('error.html')
            except:
                return render_to_response('error.html')
        else:
            return render_to_response('signin.html', {'form': form, 'registerForm': registerForm}, context_instance=RequestContext(request))
    else:
        form = LoginForm()
        return render_to_response('signin.html', {'registerForm': registerForm, 'form': form}, context_instance=RequestContext(request))


@login_required()
def system_logout(request):
    logout(request)
    return HttpResponseRedirect("/")


def create_traveller(request):
    data = request.POST
    form = TravellerRegistrationForm(data)
    response = {}
    if form.is_valid():
        response['success'] = True
        traveller = TravellerService.create(form)
        rand_password = BrainTravelUtils.id_generator()
        traveller.set_password(rand_password)
        TravellerService.save(traveller)  # Aqui se asignan los permisos
        EmailViews.send_email_confirmation(traveller, rand_password)
    else:
        message = ""
        for field, errors in form.errors.items():
            for error in errors:
                message += error

        # response['errors'] = _(message)
        response['success'] = False
        response['error'] = _(message)
        # HttpResponse(json.dumps(response))

    return JsonResponse(response)


def confirm_account(request):
    username = request.GET['username']
    hash1 = hashlib.sha256(username).hexdigest()
    hash2 = request.GET['hash']
    if hash1 == hash2:
        user = User.objects.get(username=username)
        user.is_active = True
        user.save()

        password = request.GET['rand_password']
        user_logged = authenticate(username=user.username, password=password)
        login(request, user_logged)
        return HttpResponseRedirect("/")
    else:
        return HttpResponse("Hash not math!! :(")


def cookies_policies(request):
    return render_to_response('cookies_policies.html', {}, context_instance=RequestContext(request))


def about_us(request):
    return render_to_response('about_us.html', {}, context_instance=RequestContext(request))


def privacy_terms(request):
    return render_to_response('privacy_terms.html', {}, context_instance=RequestContext(request))
