"""online_classroom_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from .views import user_register, user_login, user_logout, user_activate, user_forget_pwd, user_reset, PersonalProfile, \
    MyCourse, MyLoveOrg, MyLoveTeacher, MyLoveCourse, MyMessage, UserChangeImage,UpdateProfile

urlpatterns = [
    path('register/', user_register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('forgetpwd/', user_forget_pwd, name='forget_pwd'),
    re_path('activate/(\w+)', user_activate, name='activate'),
    re_path('reset/(\w+)', user_reset, name='reset'),
    path('personal-profile', PersonalProfile.as_view(), name='personal_profile'),
    path('my-course', MyCourse.as_view(), name='my_course'),
    path('my-love_org', MyLoveOrg.as_view(), name='my_love_org'),
    path('my-love_teacher', MyLoveTeacher.as_view(), name='my_love_teacher'),
    path('my-love_course', MyLoveCourse.as_view(), name='my_love_course'),
    path('my-message', MyMessage.as_view(), name='my_message'),
    path('update/image', UserChangeImage.as_view(), name='update_image'),
    path('update/profile', UpdateProfile.as_view(), name='update_profile'),
]
