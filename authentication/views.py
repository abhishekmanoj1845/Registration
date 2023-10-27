from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login,logout
from gfg import settings
from django.core.mail import EmailMessage, send_mail
from .models import Deparments,doctors
from .forms import BookingForm

# Create your views here.
def home(request):
    return render(request,"authentication/index.html")

def signup(request):

    if request.method == "POST":
        # username = request.POST.get('username')
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist, Please try some other username...")
            return redirect('signup')
        
        if User.objects.filter(email=email):
            messages.error(request, "Email already registered, Please try some other email address...")
            return redirect('home')
        
        if len(username)>15:
            messages.error(request,"Username must be under 15 characters")
            return redirect('signup')

        if pass1!= pass2:
            messages.error(request,"Password didn't Match")
            return redirect('signup')

        if not username.isalnum():
            messages.error(request,"Username must be alpha-numeric")
            return redirect('signup')
        else:
            myuser = User.objects.create_user(username,email,pass1)
            myuser.first_name = fname
            myuser.last_name = lname
        
            myuser.save()

            messages.success(request, " Your Account has been succesfully created... We have sent you a confirmation e-mail, please conform your account in order to activate your account")

        # Welcome Email
        subject = "Welcome to GFG- Django Login!!"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to GFG!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nAnubhav Madhav"        
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        
        return redirect('signin')
    
    return render(request,"authentication/signup.html")

def signin(request):
    if request.method == "POST":
        # username = request.POST.get('username')
        username = request.POST['username']
        pass1 = request.POST['pass1']
        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request,user)
            fname = user.first_name
            return render(request,"authentication/index.html",{'fname' : fname})
        
        else:
            messages.error(request, " Bad Credentials...")
            return redirect('signin')

    
    return render(request,"authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request,"Logged out successfully!!")
    return redirect('home')
    
    # return render(request,signout.html)

def first(request):
    return render(request,'authentication/first.html')


def Doctors(request):
    dict_docs={
        'doctor': doctors.objects.all()
    }
    return render(request,'authentication/doctors.html',dict_docs)

def department(request):
    dict_dept={
        'dept': Deparments.objects.all()
    }
    return render(request,'authentication/department.html',dict_dept)
def booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'authentication/conformation.html')
    form = BookingForm()
    dict_form ={
        "form" : form
    }
    return render(request,'authentication/booking.html  ',dict_form)
