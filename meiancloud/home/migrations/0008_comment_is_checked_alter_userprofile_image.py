# Generated by Django 4.2 on 2025-02-14 02:33

from django.db import migrations, models
import home.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_userprofile_sign_alter_userprofile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_checked',
            field=models.BooleanField(default=False, verbose_name='is_checked'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, default='home/user_img/default.png', null=True, upload_to=home.models.user_directory_path, verbose_name='头像'),
        ),
    ]
