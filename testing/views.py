from django.conf import settings
from .models import Orders
from django.shortcuts import render, redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.core.mail import send_mail
import random
from .orders import OrderForm
from .forms import Ordersforms
from django.core.files.storage import FileSystemStorage
from .otp import Otp
import requests
# Create your views hera 
def homepage(request):
    return redirect('letsconnect')
   
def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first']
        last_name = request.POST['last']
        email = request.POST['email']
        phonenumber = request.POST['phonenum']
        password = request.POST['password']
        globals()['first_name']=first_name
        globals()['last_name']=last_name
        globals()['email'] = email
        globals()['phonenumber'] = phonenumber
        globals()['password']= password
        if User.objects.filter(username=phonenumber).exists():
            messages.info(request,'PhoneNumber Taken')
            return redirect('signup')
        elif User.objects.filter(email=email).exists():
            messages.info(request,'Email taken')
            return redirect('signup')
        else:
            otp = random.randint(100000,999999)
            #user = User.objects.create_user(username=phonenumber,password=password,email=email,first_name=first_name,last_name=last_name)
            #user.save()
            globals()['otp']=otp
            send_mail('Regarding Login Into the WEBSITE',
            'Hello '  + first_name+ '  thanks for registering to the website otp has been sent to your phonenumber',
            'letsconnectsociety@gmail.com',
            [email,'dheerukreddy@gmail.com'],
            fail_silently=True,
            )
            url = "https://www.fast2sms.com/dev/bulk"

            querystring = {"authorization":"imCEKHkbYl2vGLnhstzqMZdowgQp98N3UO6DFTyu4jIVWe1JrAJ6GXvLOm12kEgyKZpqCsAjchidUVY4","sender_id":"FSTSMS","message":"OTP for login:"+str(otp),"language":"english","route":"p","numbers":phonenumber}

            headers = {
                'cache-control': "no-cache"
            }

            response = requests.request("GET", url, headers=headers, params=querystring)
            print(response)

            return redirect('verification')
        return render(request,'signup.html')
    else:
        return render(request,'signup.html')
def signuppage(request):
    return render(request,'signup.html')
def login(request):
    if request.method == 'POST':
        password = request.POST['password']
        email = request.POST['email']
        user = auth.authenticate(username=email,password=password)
        if user is not None:
            auth.login(request,user)
            return render(request,'test.html')
            
        else:
            messages.info(request,'invalid phone or password')
            return redirect('/login')
    else:
        return render(request,'test.html')
def letsconnect(request):
        return render(request,'index.html')
def logout(request):
    auth.logout(request)
    return redirect('homepage')
def verification(request):
    if request.method == 'POST':
        email_otp = int(request.POST['Email_otp'])
        try:
            user=User.objects.filter(username=phonenumber).exists()
            print(otp)
            otp is not None
        except:
            return redirect('signup')
        print(user)
        if email_otp == otp and user == False:
            messages.info(request,'otp verified')
            user = User.objects.create_user(username=phonenumber,password=password,email=email,first_name=first_name,last_name=last_name)
            user.save()
            return redirect('login')
        elif user == True:
            messages.info(request,'user salready verified')
            return redirect('login')
        else:
            messages.info(request,'otp invalid')
            return redirect('verification')
    else:
        return render(request,'verification.html')
def place_orders(request):
    if request.method == 'POST':
        upload = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(upload.name, upload)
        uploaded_file_url = fs.url(filename)
        name = request.POST["name"]
        phonenumber = request.POST["phonenumber"]
        alt_number = request.POST["alt_number"]
        address = request.POST["address"]
        landmark = request.POST["landmark"]
        print(address)
        
        orders = Orders(name=name,phonenumber=phonenumber,alt_number=alt_number,address=address,ordered=uploaded_file_url,landmark=landmark) 
        orders.save()
        url = "https://www.fast2sms.com/dev/bulk"

        querystring = {"authorization":"imCEKHkbYl2vGLnhstzqMZdowgQp98N3UO6DFTyu4jIVWe1JrAJ6GXvLOm12kEgyKZpqCsAjchidUVY4","sender_id":"FSTSMS","message":"thanks for ordering we have received your order order again","language":"english","route":"p","numbers":phonenumber}
        headers = {
            'cache-control': "no-cache"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        print(response)
        messages.info(request,'yoour order has been succesfully placed')
        return redirect('login')
        
    else:
        return redirect('signup')
def orders(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        print(user)
        orders=Orders.objects.filter(phonenumber=user)
        return render(request,"orders.html",{'orders':orders})
    else:
        return render(request,'test.html')
def test(request):

    if request.method == "POST":
        upload = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(upload.name, upload)
        uploaded_file_url = fs.url(filename)

    return render(request, 'saved.html')
def owner(request):
    if request.method == 'POST':
        password = request.POST['password']
        email = request.POST['email']
        user = auth.authenticate(username=email,password=password)
        if user is not None and user.is_staff:
            auth.login(request,user)
            return render(request,'test1.html')    
        elif user is not None:
            messages.info(request,'u r not a owner to website')
            return redirect('/owner')
        else:
            messages.info(request,'invalid phone or password')
            return redirect('/owner')
    else:
        return render(request,'test1.html')
def ordered(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        orders=Orders.objects.all().order_by('-ordered_date')
        return render(request,"ordered.html",{'orders':orders})
    else:
        return redirect('owner')
def status(request):
    if request.method == 'POST':
        
        return redirect('ordered')
    else:
        return redirect('letsconnect')