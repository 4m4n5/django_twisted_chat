from django.db import models

# Create your models here.
class ChatRoom(models.Model):
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.name
    
from django.contrib import admin
from chat.models import ChatRoom

admin.site.register(ChatRoom)