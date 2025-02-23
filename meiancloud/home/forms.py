from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from .models import Comment
from django.core.validators import RegexValidator
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

USER_GENDER_TYPE=UserProfile.USER_GENDER_TYPE

class LoginForm(forms.Form):
    username = forms.CharField(label='用户', max_length=32,widget=forms.TextInput(
        attrs={'class':'input','placeholder':'用户名',}
    ))#第一个参数是label，第二个参数是最大长度
    password = forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput(
        attrs={'class':'input','placeholder':'密码',}
    ))#第三个参数用来非明文输入

    #调用view.py中使用is_valid()时会调用clean_<field_name>方法，如果验证成功，返回cleaned_data字典，否则返回None


class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名', min_length=6, widget=forms.TextInput(
        attrs={'class': 'input', 'placeholder': '用户名只能包含字母、数字和下划线'}),
        validators=[RegexValidator(regex='^[a-zA-Z0-9_]+$',message='用户名只能包含字母、数字和下划线',
                        code='invalid_username')]
        # 用户名只能包含字母、数字和下划线
    )
    password = forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput(
        attrs={'class': 'input', 'placeholder': '密码'}
    ))
    password1 = forms.CharField(label='再次输入密码', min_length=6, widget=forms.PasswordInput(
        attrs={'class': 'input', 'placeholder': '再次输入密码'}
    ))
    nick_name = forms.CharField(label='昵称', max_length=32, widget=forms.TextInput(
        attrs={'class': 'input', 'placeholder': '昵称'}
    ))
    email = forms.EmailField(label='邮箱', widget=forms.EmailInput(
        attrs={'class': 'input', 'placeholder': '邮箱'}
    ))
    
    gender=forms.ChoiceField(choices=UserProfile.USER_GENDER_TYPE,label='性别',initial='0',
                             widget=forms.Select(attrs={'class':'input-gender'}))

    birthday=forms.DateField(widget=forms.DateInput(attrs={'class':'input input-birthday','type': 'date'}), label='出生日期', required=False)


    def clean_username(self):
        #验证用户名是否存在
        usernameGet = self.cleaned_data.get('username')
        exsits= User.objects.filter(username=usernameGet).exists()#判断用户名是否存在
        if exsits:
            raise forms.ValidationError('用户名已存在')
        if str(usernameGet)=='':
            raise forms.ValidationError('用户名不能为空')
        return usernameGet

    # 验证两次密码是否一致
    def clean_password1(self):
        passwordGet = self.cleaned_data.get('password')
        password1Get = self.cleaned_data.get('password1')
        print('passwordGet:',passwordGet)
        print('password1Get:',password1Get)
        if passwordGet != password1Get:  # 判断两次密码是否相同
            raise forms.ValidationError('两次输入的密码不一致！')
        return  password1Get
    
    def clean_gender(self):
        genderGet=self.cleaned_data.get('gender')
        if genderGet=='0':
            raise forms.ValidationError('请选择性别！')
        return genderGet


class CommentForm(forms.Form):#评论表单
    title = forms.CharField(label='标题', max_length=100, widget=forms.TextInput(
        attrs={'class': 'input', 'placeholder': '标题',}
    ),required=True)

    content = forms.CharField(label='评论', max_length=200, widget=forms.Textarea(
        attrs={'class': 'textarea', 'placeholder': '评论', 'rows': 5,
               'style':'''width: 100%; padding: 10px;border: 
               1px solid #ddd;border-radius: 4px;
               font-size: 1rem; resize:none;
               font-family:Arial, sans-serif;'''}
    ))


class ReplyForm(forms.Form):
    reply_content = forms.CharField(label='评论', max_length=200, widget=forms.Textarea(
        attrs={'class': 'textarea', 'placeholder': '回复', 'rows':5,
               'style':'''
                resize:none;
                width:98%;
                font-family:Arial, sans-serif;
                ''',}
    ))

class UserProfileForm(forms.Form):
    nick_name = forms.CharField(label='昵称', max_length=20, required=True)
    gender = forms.ChoiceField(label='性别', choices=USER_GENDER_TYPE, required=True)
    birthday = forms.DateField(label='出生日期', widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    sign = forms.CharField(label='个性签名', max_length=100, required=False, widget=forms.Textarea)

    def __init__(self,*args,**kwargs):
        userprofile=kwargs.pop('userprofile',None)
        print(kwargs)
        super().__init__(*args,**kwargs)
        print(userprofile)
        if userprofile is not None:
            self.fields['nick_name'].initial =userprofile.nick_name
            self.fields['gender'].initial =userprofile.gender
            #处理日期信息
            self.fields['birthday'].initial = str(userprofile.birthday).replace('/', '-')
            self.fields['sign'].initial =userprofile.sign
        else:
            print('错误！无法获取用户')
            raise ValueError("UnknownError")


class ChangePasswordForm(forms.Form):
    '''修改密码的表单'''
    old= forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput(
        attrs={'class': 'input', 'placeholder': '原密码'}
    ))
    new1=forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput(
        attrs={'class': 'input', 'placeholder': '新密码'}
    ))
    new2=forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput(
        attrs={'class': 'input', 'placeholder': '再次输入新密码'}
    ))
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # 从 kwargs 中获取当前用户
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not authenticate(username=self.user.username, password=old_password):
            raise forms.ValidationError("旧密码不正确")
        return old_password

    def clean_new2(self):
        new1 = self.cleaned_data.get('new1')
        new2 = self.cleaned_data.get('new2')
        if new1 and new2 and new1 != new2:
            raise forms.ValidationError("两次输入的密码不一致")
        return new2
    