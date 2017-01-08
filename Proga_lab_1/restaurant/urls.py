from django.conf.urls import url

from . import views

urlpatterns = [
    # ---------------Admin's---------------- #
    url(r'^adminka/(?P<pk>[0-9]+)/$', views.Adminka.as_view(), name='adminka'),

    # ---------------User's----------------- #
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^client/$', views.client_view, name='all_clients'),
    url(r'^client/(?P<client_id>[0-9]+)/$', views.client_view, name='client'),
    url(r'^client/(?P<client_id>[0-9]+)/order/(?P<pk>[0-9]+)$', views.OrderView.as_view(), name='order'),
    url(r'^client/(?P<client_id>[0-9]+)/new_order/$', views.new_order, name='new_order'),
]
