from django.urls import path
from django.views.generic.base import TemplateView
from . import views
app_name = 'home'  # 设置命名空间

urlpatterns = [
    path("", views.index, name="index"),
    path("findmeian/", views.findmeian, name="findmeian"),
    path("about/", views.about, name="about"),
    path("login/",views.login_view,name="login"),
    path("register/",views.register_view,name="register"),
    path('freetotalk/',views.freetotalk_view,name='freetotalk'),
    path('question/',views.question_view,name='question'),
    path('profile/<int:userid>/',views.user_profile_view,name='userprofile'),
    path('logout/',views.logout_view,name='logout'),
    path('login_prompt/',views.login_prompt_view,name='login_prompt'),
    path('changepsw/<int:userid>/',views.changepsw_view,name='changepsw'),
    path('editprofile/<int:userid>/',views.editprofile_view,name='editprofile'),
    path('delete_account/',views.delete_account,name='delete_account'),
    path('agreement/',views.user_agreement,name='user-agreement'),
    path('comment-management/', views.comment_management, name='comment-management'),
]

#XMLs
urlpatterns +=[
    path('BingSiteAuth.xml',TemplateView.as_view(template_name='xml/BingSiteAuth.xml', content_type='text/xml')),
]