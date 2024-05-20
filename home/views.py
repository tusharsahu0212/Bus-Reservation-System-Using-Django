from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from .models import UserInfo
import jwt
from datetime import datetime, timedelta
# Create your views here.

def home(request):
    
    token = request.COOKIES.get('access_token')
      
    try:
        token_data  = jwt.decode(token, "secret", algorithms="HS256")
        email = token_data['email']
        user = UserInfo.objects.get(email=email)
        return render(request, 'index.html',{'user':user})
    except Exception as e:
        print("home",e)
         
    return render(request, 'index.html',{'user':None})

def register(request):
    
    context = {}
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        age = int(request.POST['age'])
        gender = request.POST['gender']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if password==cpassword:

            try:
                user = UserInfo.objects.get(email=email)
                context['error'] = 'User already exist'  
                return render(request, 'register.html',context)
            except:
                password = make_password(password)
                user = UserInfo(first_name=first_name, last_name=last_name,age=age,gender=gender,
                                     email=email,password=password)
                user.save()
                
                payload = {
                    'email': user.email,
                    'exp': datetime.utcnow() + timedelta(minutes=20)
                }
                token = jwt.encode(payload, "secret", algorithm="HS256")
                response = render(request, 'index.html',{'user':user})
                response.set_cookie('access_token', token)
                return response
        else:
            context['error'] = 'Password dose not same'
            return render(request, 'register.html',context)


    return render(request, 'register.html')

def login(request):
    context = {}
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = UserInfo.objects.get(email=email)
            if user:
                if check_password(password, user.password):
                    payload = {
                        'email': user.email,
                        'exp': datetime.utcnow() + timedelta(minutes=20)
                    }
                    token = jwt.encode(payload, "secret", algorithm="HS256")
                    response = render(request, 'index.html',{'user':user})
                    response.set_cookie('access_token', token)   
                    return response 
                else:
                    context['error'] = 'Password dose not match'
                    return render(request, 'login.html', context)
        except:
                context['error'] = 'User dose not exist'
                return render(request, 'login.html', context)  
        
      
    return render(request, 'login.html')

def logout(request):
    token = request.COOKIES['access_token']
    try:
        token_data  = jwt.decode(token, "secret", algorithms="HS256")
        print(token_data)
        response = render(request, 'index.html',{'user':False})
        response.set_cookie('access_token', "") 
        return response
    except Exception as e:
        print("logout",e)
         
    return render(request, 'index.html',{'user':False})
