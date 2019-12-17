from django.contrib import admin
from .models import Tweeter,Relationship,Post,HistoryOfPost

# Register your models here.

admin.site.register(Tweeter)
admin.site.register(Relationship)
admin.site.register(Post)
admin.site.register(HistoryOfPost)