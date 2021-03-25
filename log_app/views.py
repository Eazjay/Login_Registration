from django.shortcuts import render, HttpResponse, redirect 
from .models import User
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'index.html')

def registration(request):
    errors =  User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            if key == 'first_name':
                messages.error(request, value, extra_tags='first_name')
            if key == 'last_name':
                messages.error(request, value, extra_tags='last_name')
            if key == 'reg_email':
                messages.error(request, value, extra_tags='reg_email')
            if key == 'reg_password':
                messages.error(request, value, extra_tags='reg_password')
            if key == 'confirm_password':
                messages.error(request, value, extra_tags='confirm_password')
        return redirect('/')
    else:
        password = bcrypt.hashpw(request.POST['reg_password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            first_name=request.POST['first_name'], 
            last_name=request.POST['last_name'], 
            email=request.POST['reg_email'], 
            password=password, 
            confirm_password=request.POST['confirm_password']
        )
        request.session['user_id'] = user.id
        request.session['is_first_time'] = True
        return redirect('/success')

def login(request):
    errors =  User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            if key == 'log_email':
                messages.error(request, value, extra_tags='log_email')
            if key == 'log_password':
                messages.error(request, value, extra_tags='log_password')
        return redirect('/')
    else:
        logged_user = User.objects.filter(email=request.POST['log_email'])
        if len(logged_user) == 0:
            messages.error(request, 'We could not find a user with that email address.', extra_tags='log_email')
            return redirect('/')
        else:
            user = logged_user[0]
            if bcrypt.checkpw(request.POST['log_password'].encode(), user.password.encode()):
                request.session['user_id'] = user.id
                return redirect('/success')
            else:
                messages.error(request, 'Password was incorrect.', extra_tags='log_password')
                return redirect('/')

def success_page(request):
    if 'is_first_time' not in request.session:
        request.session['is_first_time'] = False
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'success.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')