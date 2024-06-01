from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserAddForm
from django.contrib.auth.models import User, Group
from .decorators import admin_only, unautenticated_user
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from datetime import date, datetime
from django.contrib.auth.decorators import login_required



def Index(request):
    return render(request,"index.html")



@unautenticated_user
def SignIn(request):
    if request.method == "POST":
        username = request.POST['uname']
        password = request.POST['pswd']
        user1 = authenticate(request, username = username , password = password)
        
        if user1 is not None:
            
            request.session['username'] = username
            request.session['password'] = password
            login(request, user1)
            return redirect('Index')
        
        else:
            messages.error(request,'Username or Password Incorrect')
            return redirect('SignIn')
    return render(request,"login.html")


def SignOut(request):
    logout(request)
    return redirect('SignIn')

@login_required(login_url="SignIn")
def ListUser(request):
    contacts = User.objects.all()
    p = Paginator(contacts, 20)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)

    context = {
        'contacts':page_obj
    }

    return render(request,"user-list.html",context)


@login_required(login_url="SignIn")
def AddUser(request):
    if request.method == "POST":
        fname = request.POST["fname"]
        lname= request.POST['lname']
        email = request.POST["email"]
        uname = request.POST["uname"]
        pswd = request.POST["pswd"]
        pswd1 = request.POST["pswd1"]
        utype = request.POST['utype']

        if pswd != pswd1:
            messages.error(request,"Password Do not Matches..")
            return redirect("AddUser")
        if User.objects.filter(username = uname).exists():
            messages.error(request,"Username alredy exists user another username")
            return redirect("AddUser")
        if User.objects.filter(email = email).exists():
            messages.error(request,"Email alredy exists user another email")
            return redirect("AddUser")
        else:
            user = User.objects.create_user(first_name = fname,last_name = lname,email = email, username = uname, password =pswd)
            user.save()

            group = Group.objects.get(name=utype)
            user.groups.add(group)
            messages.success(request,"Staff added To Staff list....")
            return redirect("ListUser")
    return render(request,"user-add.html")

@login_required(login_url="SignIn")
def DeleteUser(request,pk):
    User.objects.get(id = pk).delete()
    messages.success(request,"User Data Deleted.....")
    return redirect("ListUser")






# authetication an d log out functions starts................................
@unautenticated_user
def SignUp(request):
    form = UserAddForm()
    if request.method == "POST":
        # fname = request.POST["fname"]
        # email = request.POST["email"]
        # uname = request.POST["uname"]
        # pswd = request.POST["pswd"]
        # pswd1 = request.POST["pswd1"]

        # if pswd != pswd1:
        #     messages.info(request,"Password Do not Matches..")
        #     return redirect("SignUp")
        # if User.objects.filter(username = uname).exists():
        #     messages.info(request,"Username alredy exists user another username")
        #     return redirect("SignUp")
        # if User.objects.filter(email = email).exists():
        #     messages.info(request,"Email alredy exists user another email")
        #     return redirect("SignUp")

        form = UserAddForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.save()
            group = Group.objects.get(name='student')
            user.groups.add(group)
            messages.success(request,"User Created.. Please Login....")
            return redirect("SignIn")
        
    return render(request,"register.html",{"form":form})


