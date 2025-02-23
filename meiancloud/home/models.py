from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os
import shutil
from django.conf import settings

def user_directory_path(instance, filename)->str:
    # 文件将被上传到 MEDIA_ROOT/home/user_img/{userid}/{filename}
    ext = filename.split('.')[-1]
    filename = f"{instance.owner.id}.{ext}"
    path1=os.path.join('home', 'user_img', str(instance.owner.id), filename)
    print('保存到'+path1)
    return path1

# Create your models here.
class UserProfile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE,verbose_name='用户')#包含基础的User，如用户名和密码
    # email = models.EmailField('邮箱',max_length=254,unique=True,blank=True,null=True,default='')
    nick_name = models.CharField('昵称',max_length=20,blank=True,default='')#昵称
    USER_GENDER_TYPE=(
        ('0','请选择'),('male','男'),('female','女'),('others','其他'),)
    gender=models.CharField('性别',max_length=8,choices=USER_GENDER_TYPE,default='0')
    birthday=models.DateField('出生日期',null=True,blank=True)
    image=models.ImageField(verbose_name='头像',upload_to=user_directory_path,default='home/user_img/default.png',max_length=100,blank=True,null=True)
    sign=models.TextField('个性签名',max_length=100,null=True,blank=True,default='')

    def save(self, *args, **kwargs):
        #如果图片已经存在，删除旧图片
        if self.pk:
            old_instance = UserProfile.objects.get(pk=self.pk)
            if old_instance.image and old_instance.image.name != 'home/user_img/default.png':
                old_instance.image.delete(save=False)
        #调用父类的save方法
        super().save(*args, **kwargs)

    def __str__(self):
        return self.owner.username

def delete_user_and_files(user:User):
    """
    删除用户及其相关文件
    """
    # 删除MEDIA文件夹下的用户文件
    user_media_path = os.path.join(settings.MEDIA_ROOT, 'home', 'user_img', str(user.id))
    if os.path.exists(user_media_path):
        shutil.rmtree(user_media_path)  # 递归删除文件夹

    # 删除UserProfile和User记录
    user.delete()

    # 检查
    try:
        profile = UserProfile.objects.get(owner=user)
        print("UserProfile 仍然存在！错误！")
        return False
    except UserProfile.DoesNotExist:
        print("UserProfile 已被删除！")
        return True


class Comment(models.Model):
    owner= models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name='comments',
                             verbose_name='comment_user')  # 修改这里
    title = models.TextField(max_length=50,blank=True,null=True)
    content = models.TextField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    parent_comment=models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,
                                     related_name='replies')
    # 用于标识父评论,父评论为空表示为主评论

    is_checked=models.BooleanField(verbose_name='is_checked',null=False,default=False,blank=False)
    #用作审核通过与否

    def __str__(self):
        return str(self.title)

