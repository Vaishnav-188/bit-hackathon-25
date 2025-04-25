from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm, BookingForm
from .models import Menu, Admin

def home(request):
    return render(request, 'index.html')

def userlogin(request):
    login_form = CustomAuthenticationForm()
    signup_form = CustomUserCreationForm()

    if request.method == 'POST':
        action = request.POST.get("action")

        if action == "login":
            login_form = CustomAuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, "You have successfully logged in!")
                    return redirect('menu')  # adjust to your desired page
                else:
                    messages.error(request, "Invalid credentials.")
            else:
                messages.error(request, "Login form invalid.")

        elif action == "signup":
            signup_form = CustomUserCreationForm(request.POST)
            if signup_form.is_valid():
                signup_form.save()
                messages.success(request, "Account created successfully!")
                return redirect('menu')  # adjust to your desired page
            else:
                messages.error(request, "Signup form has errors.")

    return render(request, 'userlogin.html', {
        'login_form': login_form,
        'signup_form': signup_form
    })

def adminlogin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            # Fetch user from the Admin model
            user = Admin.objects.get(username=username)

            # Check if the password matches the stored password
            if user.password == password:
                messages.success(request, "Login Successful!")
                #return redirect("dashboard/")   Redirect to the dashboard page
                return HttpResponse("Working")

            else:
                messages.error(request, "Invalid password. Try again.")

        except Admin.DoesNotExist:
            messages.error(request, "User does not exist.")

    return render(request, 'adminlogin.html')

def about(request):
    return render(request, 'about.html')

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'book.html', {'form': form})

def menu(request):
    menu_data = Menu.objects.all()
    return render(request, 'menu.html', {'menu': menu_data})

def display_menu_item(request, pk=None):
    menu_item = Menu.objects.get(pk=pk) if pk else None
    return render(request, 'menu_item.html', {'menu_item': menu_item})
