# Generated by Django 4.2 on 2025-01-31 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_remove_userprofile_birthday'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('0', '请选择'), ('male', '男'), ('female', '女'), ('others', '其他')], default='0', max_length=8, verbose_name='性别'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, default='user_img/default.png', null=True, upload_to='user_img/%Y/%m', verbose_name='头像'),
        ),
    ]
