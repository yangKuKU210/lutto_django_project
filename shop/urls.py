# from django.conf.urls import url
# from django.urls import path
# from .import views
# app_name='shop'
# urlpatterns = [
#
#
#     # path('getUserById/<str:myid>', views.getUserById, name='getUserById'),
#     url(r'^$',views.index,name='index'),
#     url(r'search/',views.search,name='search'),
#     url(r'getgoods/',views.getGoodById,name='getGoodById'),
#     url(r'goods/',views.GoodIndex,name='GoodIndex'),
# ]
from django.conf.urls import url
from django.urls import path
from .import views
app_name='shop'
urlpatterns = [


    # path('getUserById/<str:myid>', views.getUserById, name='getUserById'),
    url(r'^$',views.index,name='index'),
    url(r'search/',views.search,name='search'),
    url(r'getgoods/',views.getGoodById,name='getGoodById'),
    url(r'goods/',views.GoodIndex,name='GoodIndex'),
    url(r'addgood/',views.addGoodToCar,name='addGoodToCar'),
    url(r'delgood/',views.delGood,name='delGood'),
    url(r'account/',views.account,name='account'),
    url(r'goodcomment/', views.GoodComment, name='GoodComment'),
    url(r'delcomment/', views.DelComment, name='DelComment'),
    url(r'lovegood/', views.LoveGood, name='LoveGood'),
]