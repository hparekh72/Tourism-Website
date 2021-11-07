from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.template.loader import render_to_string, get_template
from django.utils.html import strip_tags
from django.template import Context
from django.contrib.auth.models import User
from django.views import View

from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator

# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')

def register(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already Taken')
                return redirect('register')
            else:
                email = request.POST['email']
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                #user.setPassword(password1)
                user.is_active = False
                user.save()
                a = request.user
                # print(a)
                request.session['user']=user.username
                # print(user)
                # path_to_view
                # - getting domain we are on
                # - relative url to verification
                # - encode uid
                # -token

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={'uidb64':uidb64, 'token':token_generator.make_token(user)})

                activate_url = 'http://' + domain + link

                message = render_to_string('mail_body.html', {'first_name':first_name, 'activate_url':activate_url})
                msg = EmailMessage(
                    'Tripology',
                    message,

                    settings.EMAIL_HOST_USER,
                    [user.email],
                )
                msg.content_subtype = "html"  # Main content is now text/html
                msg.send(fail_silently=False)
                messages.success(request, 'Account Successfully Created.')

                # print("Mail successfully sent")

                # print("User Added")

                return render(request, 'registration_confirmation.html')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('register')
        return redirect('/')
    else:
        return render(request, 'register.html')
#
# @csrf_exempt
# def sendEmail(request):
#     if request.method == 'POST':
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         username = request.POST['username']
#         password1 = request.POST['password1']
#         password2 = request.POST['password2']
#         email = request.POST['email']
#         if password1 == password2:
#             if User.objects.filter(username=username).exists():
#                 messages.info(request, 'Username Taken')
#                 return redirect('send_email')
#             elif User.objects.filter(email=email).exists():
#                 messages.info(request, 'Email is already Taken')
#                 return redirect('send_email')
#             else:
#
#                 user = get_user_model().objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
#                 sendConfirm(user)
#                 return render(request, 'confirm_template.html')
#         else:
#             messages.info(request, 'Password Not Matching')
#             return redirect('send_email')
#     else:
#         return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

class VerificationView(View):
    def get(self, request, uidb64, token):
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        user.is_active = True
        user.save()
        return redirect('login')