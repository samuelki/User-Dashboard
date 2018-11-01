from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login/$', views.login_page),
    url(r'^register/$', views.register_page),
    url(r'^users/login$', views.login),
    url(r'^users/register$', views.register),
    url(r'^dashboard$', views.dashboard),
    url(r'^dashboard/admin$', views.dashboard_admin),
    url(r'^users/show/(?P<id>\d+)$', views.show),
    url(r'^users/edit/(?P<id>\d+)$', views.edit),
    url(r'^users/edit$', views.edit_users),
    url(r'^users/destroy/(?P<id>\d+)$', views.destroy),
    url(r'^users/delete/(?P<id>\d+)$', views.delete),
    url(r'^message/(?P<id>\d+)$', views.message),
    url(r'^comment/(?P<user_id>\d+)/(?P<message_id>\d+)$', views.comment),
    url(r'^logout$', views.logout),
]