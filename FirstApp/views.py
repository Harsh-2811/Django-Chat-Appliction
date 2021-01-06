from django.shortcuts import render,redirect
from django.utils.safestring import mark_safe
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from . models import UserData,Room
def index(request):
    if request.user.is_authenticated:
        users = User.objects.all()

        rooms = Room.objects.filter(room_members=request.user)

        return render(request,"FirstApp/index.html",{'users':users,'rooms':rooms})
    else:
        return redirect('login')
def create_room(request):
    if request.method == "POST":
        room = Room(name = request.POST['name'],decription=request.POST['description'])
        room.save()
        members = request.POST.getlist('members','')
        for i in list(members):
           room.room_members.add(User.objects.get(id= int(i)))
        return redirect('home')

def loginprocess(request):
    if request.method == "POST":
        user  = authenticate(username=request.POST['username'],password=request.POST['password'])
        print(user)
        if user:
            login(request,user)
            request.session['User'] = user.id
            return redirect("home")
    return render(request,"FirstApp/login.html")

def register(request):
    if request.method == "POST":
        user = User.objects.create_user(username = request.POST['username'],password= request.POST['password'],
            email = request.POST['email'],first_name = request.POST['first_name'],last_name= request.POST['last_name']
        
        )
        user.save()
        udata = UserData(user=user ,Dp= request.FILES['dp'],active=False)
        udata.save()

    return redirect('login')

def room(request, room_name):
    room = Room.objects.get(name = room_name)
    members = room.room_members.all()
    userdata = UserData.objects.filter(user__in= members)


    return render(request, 'FirstApp/room.html', {
        'room_name': mark_safe(json.dumps(room_name)),
        'user_name': mark_safe(json.dumps(request.user.username)),
        'members':userdata,
        'udata':UserData.objects.get(user=request.user),

    })

def chats(request):
    return render(request,'FirstApp/chat.html')

def logoutProcesss(request):
    logout(request)
    return redirect('login')