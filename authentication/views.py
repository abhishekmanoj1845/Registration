from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login,logout,get_user_model
from gfg import settings
from .models import Deparments,doctors
from .forms import BookingForm
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage,send_mail
from .tokens import generate_token
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode




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
        
        # if User.objects.filter(email=email):
        #     messages.error(request, "Email already registered, Please try some other email address...")
        #     return redirect('home')
        
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
            myuser.is_active = False
            myuser.save()
            # myuser.save()
            # activateEmail(request,myuser,myuser.email)

            # messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        
   


            messages.success(request, " Your Account has been succesfully created... We have sent you a confirmation e-mail, please conform your account in order to activate your account")
             # Welcome Email
            subject = "Welcome to GFG- Django Login!!"
            message = "Hello " + myuser.first_name + "!! \n" + "Welcome to Appolo Hospital!! \nThank you for visiting our website.\nWe have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nAbhishek M"        
            from_email = settings.EMAIL_HOST_USER
            to_list = [myuser.email]
            send_mail(subject, message, from_email, to_list, fail_silently=True)


            # Email Address Confirmation Email
            current_site = get_current_site(request)
            email_subject = "Confirm your Email @ GFG - Django Login!!"
            message2 = render_to_string('template_activate_account.html',{
                'name': myuser.first_name,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                'token': generate_token.make_token(myuser)
            })
            email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
            )
            email.fail_silently = True
            email.send()

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
import binascii
def activate(request,uidb64,token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('signin')
    else:
        messages.error(request, 'Activation link is invalid!')
        return render(request,'activation_failed.html')



    # try:
    #     # Check length
    #     if len(uidb64) % 4 != 0:
    #         raise binascii.Error("Invalid base64 string length")

    #     # Check character set
    #     if not set(uidb64).issubset("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"):
    #         raise binascii.Error("Invalid base64 characters")

    #     uid = force_str(urlsafe_base64_decode(uidb64))
    # except (binascii.Error, TypeError):
    #     myuser = None

    # if myuser is not None and generate_token.check_token(myuser,token):
    #     myuser.is_active = True
    #     # user.profile.signup_confirmation = True
    #     myuser.save()
    #     login(request,myuser)
    #     messages.success(request, "Your Account has been activated!!")
    #     # return render(request,'authentication/index.html')

    #     return redirect('first')
    # else:
    #     print("user not generated")
    #     return render(request,'activation_failed.html')

