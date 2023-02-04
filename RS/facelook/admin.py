from django.contrib import admin
from facelook.models import *
# Register your models here.
# class TaskAdmin(admin.ModelAdmin):
#     list_display = ('name', 'creation_date', 'end_date', 'user')


#class Users(admin.ModelAdmin):
#     list_display = ('name', 'email')

# # admin.site.register(Task, User)
admin.site.register(User)
admin.site.register(Topic)

admin.site.register(Post)

admin.site.register(Like)
admin.site.register(Fallowing)