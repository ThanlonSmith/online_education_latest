import xadmin
from .models import CityInfo, OrgInfo, TeacherInfo


class CityInfoXadmin(object):
    list_display = ['name', 'add_time']
    """
    换图标：http://www.fontawesome.com.cn/
    """
    model_icon = 'fa fa-user'


class OrgInfoXadmin(object):
    list_display = ['image', 'name', 'course_num', 'study_num', 'love_num', 'click_num', 'category', 'city_info', ]
    style_fields = {'detail': 'ueditor'}  # 告诉xadmin把detail字段设置为ueditor


class TeacherInfoXadmin(object):
    list_display = ['image', 'name', 'work_year', 'work_position', 'click_num', 'age', 'gender', 'love_num', ]


xadmin.site.register(CityInfo, CityInfoXadmin)
xadmin.site.register(OrgInfo, OrgInfoXadmin)
xadmin.site.register(TeacherInfo, TeacherInfoXadmin)
