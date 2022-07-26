from email import message
from urllib import request
from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import *
from .models import Room,Topic
from .form import RoomForm , UserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.

# rooms=[
#     {'id':1, 'name':'kapil'},
#     {'id':2, 'name':'Rohit'},
#     {'id':3, 'name':'Rahul'},
# ]

def home(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    rooms=Room.objects.filter(topic__name__icontains=q)
    topic=Topic.objects.all()
    room_messages=Message.objects.filter(room__topic__name__icontains=q)
    context={'rooms':rooms, 'topic':topic,'room_messages': room_messages}
    return render(request,'base/home.html', context)

 
def room(request,pk):
    room=Room.objects.get(id=pk) 
    room_messages=room.message_set.all()
    participants=room.participants.all()
    if request.method=='POST':
        message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
    context={'room':room,'room_messages':room_messages,'participants':participants}    
    return render(request,'base/room.html',context)



# @login_required(login_url='login')
# def createroom(request):
#     form=RoomForm()
#     if request.method=='POST':
#         form= RoomForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     context={'form' : form}
#     return render(request,'base/create-room.html',context)


@login_required(login_url='login')
def createform(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        # neeche vala puchna he
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/create-room.html', context)

@login_required(login_url='login')
def updateform(request,pk):
    message=Message.objects.all()
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse("You are Not Allowed To Edit")
    if request.method=='POST':
        form= RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form, 'message':message}
    return render(request,'base/edit-user.html',context)

@login_required(login_url='login')
def deleteroom(request,pk):
    room=Room.objects.get(id=pk)
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})

def loginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')   
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request, 'user does not exit')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')

    context={}       
    return render(request,'base/login_template.html',context)

def signupPage(request):
    form=UserCreationForm()
    if request.method == 'POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            # user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
            # print('bhr hu')
        else:
            message.error(request,'error while registering')
    context={'form':form}       
    return render(request,'base/signup.html',context)


def logoutUser(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def deletemessage(request,pk):
    message=Message.objects.get(id=pk)
    if request.user!=message.user:
        return HttpResponse('you are not allowed here')
    if request.method=='POST':
        message.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':message})


# user profile
def UserProfile(request,pk):
    user=User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context={'user':user,'room_messages':room_messages,'rooms':rooms, 'topic':topics}

    # print("Context ",context)
    # return HttpResponse("response from server")

    return render(request,'base/profile.html',context)

def updateProfile(request,pk):
    user=User.objects.all()
    form=UserForm(instance=user)
    if request.method== 'POST':
        form=UserForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save
            return redirect('user-profile',pk=user.id)
    return render(request, 'base/edit-user.html')


def Topics(request):
    topics = Topic.objects.all()
    return render(request,'base/topics.html',{'topics':topics})
