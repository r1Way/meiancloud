from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile,Comment#,Reply
from django.contrib.auth.admin import UserAdmin
# Register your models here.
admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):#管理后台中以内联的方式展示和编辑 UserProfile 模型的数据。
    model = UserProfile

class UserProfileAdmin(UserAdmin):#管理后台
    inlines = [UserProfileInline]#父类就有的为空 将附加信息内联

admin.site.register(User, UserProfileAdmin)

admin.site.register(Comment)
