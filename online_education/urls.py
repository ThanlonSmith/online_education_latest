from django.contrib import admin
from django.urls import path, include
import xadmin
from apps.users.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('users/', include(('apps.users.urls', 'user'), namespace='users')),
    path('courses/', include(('apps.courses.urls', 'course'), namespace='courses')),
    path('orgs/', include(('apps.orgs.urls', 'orgs'), namespace='orgs')),
    path('operations/', include(('operations.urls', 'operations'), namespace='operations')),
    path('', index, name='index'),
    path('captcha/', include('captcha.urls')),
    path('ueditor/', include('DjangoUeditor.urls'))
]
# 配置全局404、500，变量handler404、handler500不能变，其它可以
handler404 = 'apps.users.views.page_not_found'
handler500 = 'apps.users.views.server_error'
