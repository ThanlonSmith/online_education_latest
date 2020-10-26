from django.shortcuts import render, redirect, reverse, HttpResponse
from .forms import UserRegisterForm, UserLoginForm, UserForgetPwdForm, UserResetForm, UserChangeImageForm, \
    UpdateProfileForm, UserUpdateEmailForm, UserResetEmailForm
from .models import UserProfile, EmailVerifyCode, BannerInfo
from ..orgs.models import OrgInfo
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.contrib.auth import authenticate, logout, login
from tools.send_email_tool import send_email_code
from django.views import View
from django.http import HttpResponse, JsonResponse
from ..courses.models import CourseInfo
import datetime


def index(request):
    """
    首页
    :param request: http请求对象
    :return:
    """
    """轮播图"""
    all_banner = BannerInfo.objects.order_by('-add_time')[:2]
    first_banner = BannerInfo.objects.order_by('-add_time').first()
    """课程"""
    # banner_courses = CourseInfo.objects.filter(is_banner=True)[:3]
    # all_course_info = CourseInfo.objects.filter(is_banner=False)[:3]
    all_course = CourseInfo.objects.all()[:6]
    """机构"""
    all_org = OrgInfo.objects.all()[:12]

    return render(request, 'index.html', {
        'all_banner': all_banner,
        'first_banner': first_banner,
        'all_org': all_org,
        'all_course': all_course,
        # 'banner_courses': banner_courses,
    })


# 用户注册功能模块
def user_register(request):
    if request.method == "GET":
        # 这里使用UserRegisterForm不是为了验证，而是为了使用验证码
        user_register_form = UserRegisterForm()
        return render(request, 'users/register.html', {
            'user_register_form': user_register_form
        })
    else:
        user_register_form = UserRegisterForm(request.POST)
        if user_register_form.is_valid():
            email = user_register_form.cleaned_data['email']
            password = user_register_form.cleaned_data['password']
            user_is_exists = UserProfile.objects.filter(
                Q(username=email) | Q(email=email)).exists()  # 使用 exists比使用 count 或者直接判断 QuerySet 更加高效
            if user_is_exists:
                msg = "用户已经存在，请直接 <a style='color:green;font-weight:bold' href='/users/login'>登录</a> 吧！"
                msg = mark_safe(msg)
                return render(request, 'users/register.html', {
                    'msg': msg
                })
            else:
                user = UserProfile()
                user.username = email
                user.set_password(password)
                user.email = email
                # user.image =
                user.save()
                send_email_code(email, 1)
                return HttpResponse('请尽快前往您的邮箱激活，否则无法登录！')
                # return redirect('index')
        else:
            return render(request, 'users/register.html', {
                'user_register_form': user_register_form
            })


# 用户登录功能模块
def user_login(request):
    if request.method == 'GET':
        user_login_form = UserLoginForm()
        return render(request, 'users/login.html', {
            'user_login_form': user_login_form
        })
    else:
        user_login_form = UserLoginForm(request.POST)
        if user_login_form.is_valid():
            email = user_login_form.cleaned_data['email']
            password = user_login_form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user:
                if user.is_start:
                    # return redirect('index')
                    # 可以加参数
                    login(request, user)
                    return redirect(reverse('index'))
                else:
                    return HttpResponse('请到邮箱中激活用户，否则无法登录系统！')
            return render(request, 'users/login.html', {
                'msg': '用户名或密码不正确！',
                'user_login_form': user_login_form
            })
        return render(request, 'users/login.html', {
            'user_login_form': user_login_form
        })


# 用户退出功能模块
def user_logout(request):
    logout(request)
    return redirect(reverse('users:login'))


# 用户激活(这里还遗留一个问题：如果产生的随机码有重复，一个验证码对不同的邮箱，可能会出问题)
def user_activate(request, code):
    if code:
        code_obj_list = EmailVerifyCode.objects.filter(code=code)  # <QuerySet [<EmailVerifyCode: ZW417PgB>]>
        if code_obj_list.exists():
            code_obj = code_obj_list.first()  # verify_code_obj = code_obj_list[0]
            email = code_obj.email
            user_list = UserProfile.objects.filter(username=email)
            if user_list.exists():
                user = user_list.first()
                user.is_start = True
                user.save()
                return redirect(reverse('users:login'))


# 向用户发送用于重置密码的邮箱验证码
def user_forget_pwd(request):
    if request.method == 'GET':
        user_forget_pwd_form = UserForgetPwdForm()
        return render(request, 'users/forget-pwd.html', {
            'user_forget_pwd_form': user_forget_pwd_form
        })
    else:
        user_forget_pwd_form = UserForgetPwdForm(request.POST)
        if user_forget_pwd_form.is_valid():
            email = user_forget_pwd_form.cleaned_data['email']
            user_list = UserProfile.objects.filter(email=email)
            if user_list.exists():
                send_email_code(email, 2)
                return HttpResponse('请尽快去您的邮箱重置密码！')
            else:
                return render(request, 'users/forget-pwd.html', {
                    'msg': '用户不存在！'
                })
        else:
            return render(request, 'users/forget-pwd.html', {
                'user_forget_pwd_form': user_forget_pwd_form
            })


# 重置用户密码
def user_reset(request, code):
    if code:
        if request.method == 'GET':
            return render(request, 'users/password-reset.html', {
                'code': code
            })
        else:
            user_reset_form = UserResetForm(request.POST)
            if user_reset_form.is_valid():
                password = user_reset_form.cleaned_data['password']
                password2 = user_reset_form.cleaned_data['password2']
                if password == password2:
                    code_obj_list = EmailVerifyCode.objects.filter(
                        code=code)  # <QuerySet [<EmailVerifyCode: VmUIe9CS>]>
                    if code_obj_list.exists():
                        email = code_obj_list.first().email
                        user_obj_list = UserProfile.objects.filter(email=email)
                        if user_obj_list.exists():
                            current_user = user_obj_list.first()
                            print(current_user)
                            current_user.set_password(password)
                            current_user.save()
                            return redirect(reverse('users:login'))
                        else:
                            pass
                    else:
                        pass
                else:
                    return render(request, 'users/password-reset.html', {
                        'msg': '两次密码不一致！',
                        'code': code
                    })
            else:
                return render(request, 'users/password-reset.html', {
                    'user_reset_form': user_reset_form,
                    'code': code
                })
    pass


# 个人资料
class PersonalProfile(View):
    def get(self, request):
        return render(request, 'users/personal_profile.html', {
            'item_name': '个人资料',
        })


# 用户头像的修改
class UserChangeImage(View):
    def post(self, request):
        # instance：指名实例是什么？做修改的时候，我们需要知道是给哪个对象实例进行修改。如果不指名，就会被当做创建对象去执行
        user_change_image_form = UserChangeImageForm(request.POST, request.FILES,
                                                     instance=request.user)  # request.FILES：post以外的数据
        if user_change_image_form.is_valid():
            user_change_image_form.save(commit=True)  # 修改，如果加是不知道创建还是修改
            return JsonResponse({
                'status': 'ok'
            })
        else:
            return JsonResponse({
                'status': 'fail'
            })


# 获取邮箱验证码
class GetEmailCode(View):
    '''
    当用户修改邮箱，点击获取验证码的时候，会通过这个函数处理，发送邮箱验证码
    :param request: http请求对象
    :return: 返回json数据，在模板页面当中去处理
    '''

    def post(self, request):
        user_update_email_form = UserUpdateEmailForm(request.POST)
        if user_update_email_form.is_valid():
            email = user_update_email_form.cleaned_data['email']
            user_list = UserProfile.objects.filter(Q(email=email) | Q(username=email))
            if user_list.exists():
                return JsonResponse({'status': 'fail', 'msg': '邮箱已经被绑定'})
            else:
                # 我们在发送邮箱验证码之前，应该去邮箱验证码的表当中去查找，看之前有没有往当前这个邮箱发送过修改邮箱这个类型的验证码
                email_ver_list = EmailVerifyCode.objects.filter(email=email, send_type=3)
                # 如果发送过验证码，那么我们就拿到最近发送的这一个
                if email_ver_list.exists():
                    email_first = email_ver_list.order_by('-add_time')[0]
                    # 判断当前时间和最近发送的验证码添加时间之差
                    if (datetime.datetime.now() - email_first.add_time).seconds > 60:
                        # 如果我们重新发送了新的验证码，那么以前最近发的就被清了
                        send_email_code(email, 3)
                        email_first.delete()
                        return JsonResponse({'status': 'ok', 'msg': '请尽快去邮箱当中获取验证码！'})
                    else:
                        return JsonResponse({'status': 'fail', 'msg': '请不要重复发送验证码，1分钟后重试！'})
                else:
                    send_email_code(email, 3)
                    return JsonResponse({'status': 'ok', 'msg': '请尽快去邮箱当中获取验证码'})
        else:
            return JsonResponse({'status': 'fail', 'msg': '您的邮箱有问题'})


# 重置邮箱
class ResetEmail(View):
    def post(self, request):
        user_reset_email_form = UserResetEmailForm(request.POST)
        if user_reset_email_form.is_valid():
            email = user_reset_email_form.cleaned_data['email']
            code = user_reset_email_form.cleaned_data['code']
            email_verify_code_list = EmailVerifyCode.objects.filter(email=email, code=code)
            if email_verify_code_list.exists():
                email_ver = email_verify_code_list[0]
                if (datetime.datetime.now() - email_ver.add_time).seconds < 60:
                    request.user.username = email
                    request.user.email = email
                    request.user.save()
                    return JsonResponse({'status': 'ok', 'msg': '邮箱修改成功！'})
                else:
                    return JsonResponse({'status': 'fail', 'msg': '验证码失效，请重新发送验证码！'})
            else:
                return JsonResponse({'status': 'fail', 'msg': '邮箱或者验证码有误'})
        else:
            return JsonResponse({'status': 'fail', 'msg': '邮箱或者验证码不合法'})


# 更新个人资料
class UpdateProfile(View):
    def post(self, request):
        # nick_name = request.POST.get('nick_name')
        # birthday = request.POST.get('birthday')
        # gender = request.POST.get('gender')
        # address = request.POST.get('address')
        # phone = request.POST.get('phone')
        update_profile_form = UpdateProfileForm(request.POST, instance=request.user)
        ret = {'status': None, 'msg': None}
        if update_profile_form.is_valid():
            update_profile_form.save(commit=True)
            ret['status'] = 'ok'
            ret['msg'] = '修改成功！'
            return JsonResponse(ret)
        else:
            print(
                update_profile_form.errors)  # <ul class="errorlist"><li>birthday<ul class="errorlist"><li>输入一个有效的日期。</li></ul></li></ul>
            ret['status'] = 'fail'
            ret['msg'] = '修改失败！'
            return JsonResponse(ret)


# 我的课程
class MyCourse(View):
    def get(self, request):
        return render(request, 'users/my_course.html', {
            'item_name': '我的课程'
        })


# 我的收藏-课程机构
class MyLoveOrg(View):
    def get(self, request):
        return render(request, 'users/my_love_org.html', {
            'item_name': '我的收藏'
        })


# 我的收藏-授课教师
class MyLoveTeacher(View):
    def get(self, request):
        return render(request, 'users/my_love_teacher.html', {
            'item_name': '我的收藏'
        })


# 我的收藏-公开课程
class MyLoveCourse(View):
    def get(self, request):
        return render(request, 'users/my_love_course.html', {
            'item_name': '我的收藏'
        })


# 我的消息
class MyMessage(View):
    def get(self, request):
        return render(request, 'users/my_message.html', {
            'item_name': '我的消息'
        })
