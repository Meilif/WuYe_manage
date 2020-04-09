from django.urls import path
from django.conf.urls import url
from mainApp import views

app_name = '[mainApp]'


urlpatterns = [
    url(r'^$', views.login),
    path('index/', views.index, name='index'),
    path('base/', views.base, name='base'),
    path('login/', views.login, name='login'),
    path('order/<int:status>/', views.order, name='order', ),
    path('ann/', views.announce, name='ann'),
    path('user/', views.user, name='user'),
    path('logout/', views.logout, name='logout'),
    path('cre_ord/', views.cre_ord, name='cre_ord'),
    path('cre_ann/', views.cre_ann, name='cre_ann'),
    path('cre_user/', views.cre_user, name='cre_user'),
    path('alter_user/<int:uid>/', views.alter_user, name='alter_user'),
    path('alter_order/<int:uid>/', views.alter_ord, name='alter_ord'),
    path('alter_ann/<int:uid>/', views.alter_ann, name='alter_ann'),
    path('update/user/<int:uid>/', views.alter_user, name='update_user'),
    path('catch_ord/<int:uid>/', views.catch_order, name='catch_order'),
    path('refer_ord/<int:uid>/', views.refer_order, name='refer_order'),
    path('pass_ord/<int:uid>/<int:status>/', views.pass_order, name='pass_ord'),
    path('del_user/<int:uid>/', views.del_user, name='del_user'),
    path('del_ord/<int:uid>/', views.del_ord, name='del_ord'),
    path('del_ann/<int:uid>/', views.del_ann, name='del_ann'),
]
