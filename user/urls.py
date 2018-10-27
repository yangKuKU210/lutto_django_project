from django.conf.urls import url
from django.urls import path
from .import views
app_name='user'
urlpatterns = [


    # 登录
    url(r'login/', views.login, name='login'),
    # 获取用户信息by id
    url(r'^getUser\w*/(?P<myid>\d+)', views.getUserById, name='getUserById'),
    url(r'^$', views.index, name='index'),
    # 注册
    url(r'regist/', views.regist_ser, name='regist'),
    # 修改密码
    url(r'change/', views.changePassword, name='changePassword'),
    #
    url(r'userinfo/', views.userInfo, name='userInfo'),
    # 修改用户信息
    url(r'upuser/', views.UpUser, name='UpUser'),
    # 给课程添加评论
    url(r'addcoursecomment/', views.addCourseComment, name='addCourseComment'),
    # 给评论点赞
    url(r'likecoursecomment/', views.likeCourseComment, name='likeCourseComment'),
    # 添加地址
    url(r'useraddress/',views.UserAddress,name='UserAddress'),
    # 删除地址
    url(r'deladdress/',views.delAddress,name='delAddress'),
    # 获取用户详细信息 by电话号
    url(r'getuserinfobytel/', views.GetNameByTel, name='GetNameByTel'),
    # 获取地址
    url(r'getaddress/', views.GetAddress, name='GetAddress'),

    url(r'upload/', views.upload, name='upload'),
    url(r'qiniutoken/', views.qiniuToken, name='qiniuToken'),

    # 用户添加训练课程
    url(r'getaction/', views.Getaction, name='Getaction'),
    # 用户删除训练课程
    url(r'delaction/', views.DelAction, name='DelAction'),
    # 用户收藏商品
    url(r'getlove/', views.GetLove, name='GetLove'),
    # 用户删除收藏商品
    url(r'dellove/', views.DelLove, name='DelLove'),
    url(r'qiandao/', views.QianDao, name='QianDao'),
    url(r'upicon/', views.upIcon, name='upIcon'),
    url(r'sendcode/', views.SendCode, name='SendCode'),
    url(r'checkcode/', views.CheckCode, name='CheckCode'),
    # url(r'getlove/', views.GetLoveGood, name='GetLoveGood'),

]