from django.shortcuts import redirect, reverse
from django.http import JsonResponse


def login_decorator(func):
    def inner(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            if request.is_ajax():
                return JsonResponse({'status': 'nologin'})
            # 获取目前访问的url
            url = request.get_full_path()
            ret = redirect(reverse('users:login'))
            ret.set_cookie('url', url)
            return ret

    return inner


"""
@login_decorator
def f():
    pass
"""

# f = login_decorator(f)
