from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *

def index(request):
    if 'id' in request.session:
        return redirect('/dashboard')

    return render(request, 'users/index.html')

def login_page(request):
    return render(request, 'users/login.html')

def register_page(request):
    return render(request, 'users/register.html')

def dashboard(request):
    if 'id' not in request.session:
        return redirect('/')

    context = {
        'logged_user': User.objects.get(id=request.session['id']),
        'user_data': User.objects.all()
    }

    return render(request, 'users/dashboard.html', context)

def dashboard_admin(request):
    return render(request, 'users/dashboard_admin/html', {'user_data': User.objects.all()})
    
def show(request, id):
    user = User.objects.get(id=id)
    context = {
        'user': user,
        'message_data': Message.objects.filter(for_user=user),
        'comment_data': Comment.objects.all(),
        'logged_user': User.objects.get(id=request.session['id'])
    }

    return render(request, 'users/profile.html', context)

def register(request):
    if request.method != 'POST':
        return redirect('/')

    errors = User.objects.validator(request.POST)
    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error)
        return redirect('/register')

    user = User.objects.create_user(request.POST)

    if 'user_level' not in request.session:
        request.session['id'] = user.id
        request.session['user_level'] = user.user_level
        return redirect('/users/show/'+str(request.session['id']))
    elif request.session['user_level'] == 0:
        request.session['id'] = user.id
        request.session['user_level'] = user.user_level
        return redirect('/users/show'+str(request.session['id']))
    elif request.session['user_level'] == 9:
        return redirect('/users/show/'+str(user.id))

def login(request):
    if request.method != 'POST':
        return redirect('/login')

    valid, response, user_level = User.objects.login(request.POST)
    if valid == True:
        request.session['id'] = response
        request.session['user_level'] = user_level
        return redirect('/users/show/'+str(request.session['id']))
    else:
        messages.error(request, response)

    return redirect('/login')

def logout(request):
    request.session.clear()
    return redirect('/login')

def edit(request, id):
    context = {
        'user_data': User.objects.filter(id=id),
        'logged_user': User.objects.get(id=request.session['id'])
    }
    return render(request, 'users/edit.html', context)

def edit_users(request):
    if request.method != 'POST':
        return redirect('/edit')

    user = User.objects.get(id=request.POST['id'])
    if request.POST['submit'] == 'Save':
        errors = User.objects.update_validator(request.POST)
        if len(errors) > 0:
            for tag, error in errors.items():
                messages.error(request, error)
            return redirect('/users/edit/'+str(user.id))
        else:
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.user_level = request.POST['user_level']
            user.save()
            return redirect('/dashboard')

    if request.POST['submit'] == 'Update Password':
        errors = User.objects.pw_validator(request.POST)
        if len(errors) > 0:
            for tag, error in errors.items():
                messages.error(request, error)
            return redirect('/users/edit/'+str(user.id))
        else:
            User.objects.update_pw(request.POST)
            return redirect('/dashboard')

    if request.POST['submit'] == 'Save Description':
        user.description = request.POST['description']
        user.save()
        return redirect('/dashboard')

def destroy(request, id):
    user = User.objects.get(id=id)
    context = {
        'user': user,
        'logged_user': User.objects.get(id=request.session['id'])    
    }
    return render(request, 'users/confirm_delete.html', context)

def delete(request, id):
    User.objects.get(id=id).delete()
    return redirect('/dashboard')

def message(request, id):
    from_user = User.objects.get(id=request.session['id'])
    for_user = User.objects.get(id=id)
    message = request.POST['message']
    Message.objects.create(message=message, from_user=from_user, for_user=for_user)
    return redirect('/users/show/'+str(id))

def comment(request, user_id, message_id):
    message = Message.objects.get(id=message_id)
    user = User.objects.get(id=request.session['id'])
    comment = request.POST['comment']
    Comment.objects.create(user=user, comment=comment, message=message)
    return redirect('/users/show/'+str(user_id))