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
    # path('getUserById/<str:myid>', views.getUserById, name='getUserById'),
    url(r'^$', views.index, name='index'),
    url(r'search/', views.search, name='search'),
    url(r'getgoods/', views.getGoodById, name='getGoodById'),
    url(r'goods/', views.GoodIndex, name='GoodIndex'),
    url(r'addgood/', views.addGoodToCar, name='addGoodToCar'),
    url(r'delgood/', views.delGood, name='delGood'),
    url(r'account/', views.account, name='account'),
    url(r'goodcomment/', views.GoodComment, name='GoodComment'),
    url(r'delcomment/', views.DelComment, name='DelComment'),
    url(r'mylove/', views.LoveGood, name='LoveGood'),
    url(r'getcart/', views.GetCart, name='GetCart'),
    url(r'getcomment/', views.GetGoodComment, name='GetGoodComment'),
    url(r'likecomment/', views.likeComment, name='likeComment'),
    url(r'returncomment/', views.ReturnComment, name='ReturnComment'),
    url(r'makeorder/', views.OrderGood, name='OrderGood'),
    url(r'delorder/', views.DelOrder, name='DelOrder'),
    url(r'getorder/', views.GetOrder, name='GetOrder'),
    url(r'dealorder/', views.DealOrder, name='DealOrder'),

]