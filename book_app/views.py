from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def form(request):
    return render(request, 'login.html')

def success(request): 
    context={
        "all_books": Book.objects.all(),
        "user": User.objects.get(id=request.session['user_id']),
    }
    return render(request, 'all_books.html', context)

def registered(request):

    errors = User.objects.basic_validator(request.POST)

    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")

    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)

        request.session['user_id'] = user.id

        return redirect("/success")

def logout(request):
    request.session.flush()
    return redirect('/')

def login(request):

    user = User.objects.filter(email=request.POST['email'])

    if len(user)>0:
        logged_user = user[0]

        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            
            return redirect ("/success")
        
    else:
        messages.error(request, "Password and email do not match")
        return redirect("/")

def add_book(request):
    errors = Book.objects.book_validator(request.POST)

    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/success')
    else:
        user = User.objects.get(id=request.session['user_id'])
        new_book = Book.objects.create(
                title=request.POST['title'], 
                description = request.POST['description'], 
                uploaded_by=user
            )
        request.session['book_id'] = new_book.id
        new_book.save()
        user.liked_books.add(new_book)
        
        return redirect('/success')

def onebook(request, book_id):
    context = {
        "book": Book.objects.get(id=book_id),
        "user": User.objects.get(id=request.session['user_id']),
    }
    return render (request, 'one_book.html', context)

def favorite(request, book_id):
    user = User.objects.get(id=request.session['user_id'])
    this_book = Book.objects.get(id=book_id)
    user.liked_books.add(this_book)

    return redirect('/favorites')

def favorites_page(request):
    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "all_books": Book.objects.all(),
    }

    return render (request, 'favorites.html', context)

def unfavorite(request, book_id):
    user= User.objects.get(id=request.session['user_id'])
    book= Book.objects.get(id=book_id)
    user.liked_books.remove(book)

    return redirect(f'/book/{book_id}')

def update(request,book_id):
    errors = Book.objects.book_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/book/{book_id}")
    else:
        updated = Book.objects.get(id=book_id)
        if request.method == "POST":
            updated.title = request.POST.get('title')
            updated.description = request.POST.get('description')
        updated.save()
        return redirect("/success")

def delete(request, book_id):
    Book.objects.get(id=book_id).delete()
    return redirect('/success')