from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse,HttpRequest
from django.shortcuts import render, redirect, get_object_or_404 
from .forms import LoginForm, RegisterForm, CommentForm, ReplyForm,ChangePasswordForm,UserProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import delete_user_and_files
from .models import UserProfile, Comment
from django.http import JsonResponse
from django.contrib import messages

def get_userprofile(request:HttpRequest):
    '''由request获取昵称'''
    nickname=None
    user_profile=None
    if request.user.is_authenticated and (not request.user.is_superuser):
        try:
            user_profile = UserProfile.objects.get(owner=request.user)
            nickname = user_profile.nick_name
        except UserProfile.DoesNotExist:
            nickname='None'
    elif request.user.is_superuser:
        nickname=request.user.username
    return nickname, user_profile

def default_context(request:HttpRequest):
    nickname,userprofile=get_userprofile(request)
    d={'nick_name':nickname,
       'user':request.user,
       'userprofile':userprofile,}
    return d


def index(request:HttpRequest):
    '''主页视图'''
    # 直接使用render函数来渲染模板并返回响应
    context=default_context(request)
    return render(request, "home/index.html", context)

def findmeian(request:HttpRequest):
    '''循迹梅庵视图'''
    context=default_context(request)
    return render(request,"home/findmeian.html", context)

def about(request:HttpRequest):
    '''关于我们视图'''
    context=default_context(request)
    return render(request,"home/about.html", context)
    
def freetotalk_view(request:HttpRequest):
    '''评论区视图'''
    comment_form=None
    reply_form=None
    #success=0
    if request.method=='POST':
        action_type = request.POST.get('action_type')#判定是提交评论还是提交回复
        if action_type == 'action1':
            print('提交评论')
            # 处理评论操作
            comment_form=CommentForm(request.POST)
            reply_form=ReplyForm()
            if comment_form.is_valid():
                #comment =comment_form.save(commit=False)
                print('comment有效')
                if request.user.is_authenticated and (not request.user.is_superuser):
                    # 如果已经登录了
                    print('登录了')
                    user_profile = UserProfile.objects.get(owner=request.user)#获取user对应的user_profile
                    title=request.POST.get('title')
                    content=request.POST.get('content')
                    Comment.objects.create(owner=user_profile,title=title,content=content,parent_comment=None)
                    #success=1
                    #return redirect(request.path)
                    return JsonResponse({'success': True})
                else:
                    print('没有登录')
                    return redirect('home:login_prompt')
            else:
                return JsonResponse({'success': False, 'errors': comment_form.errors})
        else:
            # 处理提交回复
            #reply_form=CommentForm(request.POST)
            print('开始处理回复')
            comment_form=CommentForm()
            reply_form=ReplyForm(request.POST)
            if reply_form.is_valid():
                #reply=reply_form.save(commit=False)
                if request.user.is_authenticated and (not request.user.is_superuser):
                    comment_id = request.POST.get('comment_id')
                    print('commentid'+f'{comment_id}')
                    comment = get_object_or_404(Comment, id=comment_id)
                    reply_content = reply_form.cleaned_data['reply_content']
                    user_profile = UserProfile.objects.get(owner=request.user)  # 获取user对应的user_profile
                    Comment.objects.create(owner=user_profile,title=None,content=reply_content,parent_comment=comment)
                    print('创建了回复')
                    #success=2
                    return JsonResponse({'success': True,'action':'reply'})
                    
                else:
                    print('没有登录')
                    return redirect('home:login_prompt')
            else:
                print('错误！')
                return JsonResponse({'success': False, 'errors': reply_form.errors})
    elif request.method == 'DELETE':
        try:
            # 获取要删除的评论 ID
            comment_id = request.GET.get('comment_id')  # 从请求中获取评论 ID
            comment = get_object_or_404(Comment, id=comment_id)
            
            # 如果评论是父评论，删除所有子评论
            if comment.parent_comment is None:
                comment.replies.all().delete()
            
            # 删除评论本身
            comment.delete()
            
            return JsonResponse({'status': 'success', 'message': '评论删除成功'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        comment_form=CommentForm()
        reply_form=ReplyForm()
        #return JsonResponse({'status': 'None', 'message': '评论删除成功'})
    
     # 获取所有主评论并关联用户信息
    comment_list = Comment.objects.all().filter(parent_comment__isnull=True,is_checked=True).select_related('owner__owner').prefetch_related('replies').order_by('-id')
    # 获取审核过的评论
    for comment in comment_list:
        comment.filtered_replies = comment.replies.filter(is_checked=True)
    paginator = Paginator(comment_list, 5)  # 每页显示5条评论
    page_number = request.GET.get('page')
    comments = paginator.get_page(page_number)

    context=default_context(request)
    context.update({
        'comment_form': comment_form,
        "comments": comments,
        'reply_form': reply_form,

    })
    return render(request,'home/freetotalk.html', context)

def question_view(request:HttpRequest):
    '''Q&A视图'''
    context=default_context(request)
    return render(request,'home/question.html', context)

def login_view(request:HttpRequest):
    '''登录界面视图'''
    success=False
    if request.method != 'POST':
        form = LoginForm()
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)#登录
                success=True
            else:
                # 添加错误信息
                form.add_error(field=None,error='用户名或密码错误！')
    print(form.non_field_errors())
    context=default_context(request)
    context.update({'form': form,'success':success})
    return render(request, 'home/login.html', context)


def register_view(request:HttpRequest):
    '''注册界面视图'''
    success=False
    if request.method != 'POST':
        form =RegisterForm()
    else:
        form=RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            nick_name = form.cleaned_data['nick_name']
            gender=form.cleaned_data['gender']
            birthday=form.cleaned_data['birthday']

            # 创建User对象
            user = User.objects.create_user(username=username, password=password, email=email)
            # 创建UserProfile对象
            UserProfile.objects.create(owner=user,nick_name=nick_name,gender=gender,birthday=birthday)

            # 登录用户
            login(request, user)
            success=True
            
        else:
            print('注册失败')
            pass
    context=default_context(request)
    context.update({'form': form,'success':success})
    return render(request, 'home/register.html',context)

#注销界面
def logout_view(request:HttpRequest):
    '''注销界面视图'''
    logout(request)
    return redirect('home:index')

#登录中转界面
def login_prompt_view(request:HttpRequest):
    '''登录中转界面视图'''
    context=default_context(request)
    return render(request,'home/login_prompt.html',context=context)

#用户界面
# @login_required(login_url='home:login_prompt')
def user_profile_view(request:HttpRequest,userid:int):
    '''用户界面视图'''
    user_profile1=None # 需要展现的userprofile
    #current_user=None #需要展现的user
    if request.user.is_authenticated:
        if request.user.id==userid and (not request.user.is_superuser):
            user_profile1 = get_object_or_404(UserProfile, owner=request.user)
            if user_profile1 is not None:
                context=default_context(request)
                context.update({
                    'current_userprofile': user_profile1,
                    'current_user':get_object_or_404(User,id=userid),
                })
                return render(request, 'home/userprofile.html', context)
        else:
            user0=get_object_or_404(User,id=userid)
            user_profile1=get_object_or_404(UserProfile,owner=user0)
            if user_profile1 is not None:
                context=default_context(request)
                context.update({
                    'current_userprofile': user_profile1,
                    'current_user':user0,
                })
            return render(request, 'home/userprofile.html', context)
    elif (not request.user.is_authenticated) or request.user.id!=userid:
        user0=get_object_or_404(User,id=userid)
        user_profile1=get_object_or_404(UserProfile,owner=user0)
        if user_profile1 is not None:
            context=default_context(request)
            context.update({
                'current_userprofile': user_profile1,
                'current_user':user0,
            })
            return render(request, 'home/userprofile.html', context)
    else:
        print('错误！')
        return redirect('home:login_prompt')
        

@login_required(login_url='home:login')
def changepsw_view(request:HttpRequest,userid:int):
    if request.user.id==userid:
        form=None
        success=False
        if request.method=='POST':
            form=ChangePasswordForm(request.POST,user=request.user)
            if form.is_valid():
                # 更新密码
                user = request.user
                user.set_password(form.cleaned_data['new1'])
                user.save()
                print('修改了密码')
                success=True
                #退出登录
                logout(request)
            else:
                print('修改密码失败')
                success=False
                
        else:
            form=ChangePasswordForm()
        
        context=default_context(request)
        context.update({
            'form':form,
            'success':success,
        })
        return render(request,'home/changepassword.html',context)
    else:
        return redirect('home:login_prompt')
    
@login_required(login_url='home:login_prompt')
def editprofile_view(request:HttpRequest,userid:int):
    if request.user.id==userid:
        form=None
        success=False
        user_profile = get_object_or_404(UserProfile, owner=request.user)
        #print(user_profile)
        print(user_profile.image.url)
        if request.method=='POST':
            form=UserProfileForm(request.POST,userprofile=user_profile)
            if form.is_valid():
                # 如果表单有效，更新信息
                user_profile.nick_name = form.cleaned_data['nick_name']
                user_profile.gender = form.cleaned_data['gender']
                user_profile.birthday = form.cleaned_data['birthday']
                user_profile.sign = form.cleaned_data['sign']

                # 处理头像上传，如果用户上传了新的头像

                if 'image' in request.FILES:
                    print('上传了头像',request.FILES['image'])
                    user_profile.image = request.FILES['image']
                
                user_profile.save()  # 保存到数据库
                # 更新成功后重定向到用户资料页面
                success=True
                #return redirect('home:userprofile',userid=userid)  
        else:
            form=UserProfileForm(userprofile=user_profile)
            success=False

        context=default_context(request)
        context.update({
            'form':form,
            'userprofile':user_profile,
            'success':success
        })
        return render(request,'home/editprofile.html',context)
    else:
        return redirect('home:login_prompt')


@login_required(login_url='home:login')
def delete_account(request:HttpRequest):
    '''
    注销账户并删除有关数据
    '''
    if request.method == 'POST':
        password = request.POST.get('password')
        user = request.user

        # 验证密码
        if authenticate(username=user.username, password=password):
            # 密码正确，执行注销操作
            if delete_user_and_files(user):
                logout(request)
                print('注销成功！')
                return JsonResponse({'success': True})
        else:
            # 密码错误
            return JsonResponse({'success': False, 'error': '密码错误'})
    return JsonResponse({'success': False, 'error': '无效请求'})
    

def user_agreement(request:HttpRequest):
    '''用户协议'''
    context=default_context(request)
    return render(request,'home/user-agreement.html',context)


@user_passes_test(lambda u: u.is_superuser)
def comment_management(request:HttpRequest):
    if request.method == 'POST':
        if 'approve' in request.POST:
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(Comment, id=comment_id)
            comment.is_checked = True
            comment.save()
            #messages.success(request, '评论已审核通过')
        elif 'delete' in request.POST:
            comment_id = request.POST.get('comment_id')  # 从请求中获取评论 ID
            # 开始删除
            print(comment_id)
            comment = get_object_or_404(Comment, id=comment_id)
            
            # 如果评论是父评论，删除所有子评论
            if comment.parent_comment is None:
                comment.replies.all().delete()
            # 删除评论本身
            comment.delete()

    comments = Comment.objects.all().order_by('-id')
    context=default_context(request)
    context.update({'comments': comments})
    return render(request, 'home/comment_management.html', context)