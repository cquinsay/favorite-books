from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, 'index.html')


def register(request):
    errors = User.objects.user_validator(request.POST)
    if request.method == "POST":
        if User.objects.filter(email = request.POST['email']):
            messages.error(request, 'That email already exists!')
            return redirect('/')
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode() 

            new_user = User.objects.create(
                first_name=request.POST['first_name'], 
                last_name=request.POST['last_name'], 
                email=request.POST['email'], 
                password=pw_hash
            )
            request.session['user_id'] = new_user.id
            request.session['user_name']=f"{new_user.first_name}"
            return redirect("/books") # never render on a post, always redirect!    
    return redirect('/')


def books(request):
    if 'user_id' in request.session:
        user = User.objects.filter(id=request.session['user_id'])
        if user:
            context = {
                'user': user[0],
                'books':Book.objects.all(),
            }
            return render(request, 'main.html', context)
    return redirect('/')


def login(request):
    errors = User.objects.login_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['login_email'])
        request.session['user_id'] = user.id
        request.session['user_name']=f"{user.first_name}"
        
        return redirect('/books')
    return redirect("/")

def logout(request):
    request.session.clear()

    return redirect('/')

def add_book(request):
    errors = Book.objects.book_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/books')
    else:
        user = User.objects.get(id=request.session['user_id'])
        book = Book.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            book_adder=user
        )
        user.favorited_books.add(book)
        
        return redirect(f'/books/{book.id}')


def book_info(request, book_id):
    context = {
        'book': Book.objects.get(id=book_id),
        'logged_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, "book_info.html", context)


def update(request, book_id):
    book = Book.objects.get(id=book_id)
    book.description = request.POST['description']
    book.save()

    return redirect(f"/books/{book_id}")


def delete(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return redirect('/books')


def favorite(request, book_id):
    user = User.objects.get(id=request.session["user_id"])
    book = Book.objects.get(id=book_id)
    user.favorited_books.add(book)

    return redirect(f'/books/{book_id}')


def unfavorite(request, book_id):
    user = User.objects.get(id=request.session["user_id"])
    book = Book.objects.get(id=book_id)
    user.favorited_books.remove(book)

    return redirect(f'/books/{book_id}')

    
    def home(request):
        return redirect('books')



