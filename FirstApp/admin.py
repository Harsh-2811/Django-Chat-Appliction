from django.contrib import admin
from .models import Chat,UserData,Room
# Register your models here.
admin.site.register(Chat)
admin.site.register(Room)
admin.site.register(UserData)
