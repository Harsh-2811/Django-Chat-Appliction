from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
User=get_user_model()
# Create your models here.
class UserData(models.Model):
    user = models.OneToOneField(User,related_name="+",primary_key=True,on_delete=models.CASCADE)
    Dp= models.ImageField(upload_to="Chatapp")
    active = models.BooleanField(default=False)
    last_seen = models.DateTimeField(default=datetime.now())
    def __str__(self):
        return self.user.username

class Room(models.Model):
    
    name = models.CharField(default="",max_length=100)
    room_members = models.ManyToManyField(User)
    decription = models.TextField(default="",max_length=200)
    created_at = models.DateTimeField(default=datetime.now())
    def __str__(self):
        return self.name
    

class Chat(models.Model):
    name=models.ForeignKey(User,related_name='author_message',on_delete=models.CASCADE)
    msg=models.CharField(max_length=100)
    timestamp=models.TimeField(auto_now_add=True)
    room = models.ForeignKey(Room,on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name.username
