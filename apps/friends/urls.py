from django.conf.urls import url
##from django.contrib import admin
from . import views

urlpatterns = [
  url(r'^$', views.main, name='index'),
  url(r'^friends$', views.success, name='success'),
  url(r'^user/(?P<id>\d+)$', views.profile, name='profile'),
  url(r'^register$', views.register, name='register'),
  url(r'^login$', views.login, name='login'),
  url(r'^logout$', views.logout, name='logout'),
  url(r'^remove/(?P<id>\d+)$', views.remove, name='remove'),
  url(r'^add/(?P<id>\d+)$', views.add, name='add'),
    # url(r'^this_app/(?P<id>\d+)/edit$', views.edit, name='my_edit'),
    # url(r'^this_app/(?P<id>\d+)/delete$', views.delete, name='my_delete'),
    # url(r'^this_app/(?P<id>\d+)$', views.show, name='my_show'),
]
