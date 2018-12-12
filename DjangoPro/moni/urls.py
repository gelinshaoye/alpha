#coding=utf-8
from django.conf.urls import url
from .views import *

urlpatterns = [
    url('^login/$',Login,name='Login'),
    url('^login_handle/$',Login_handle),
    url('^login_out/$',Logout),
    url('^index/$',Index,name='Index'),
    url('^monimchinfo/$',MoniMchInfo),
    url('^monimchinfohandle/$',MoniMchInfoHandle),
    url('^avgpage/$', MoniAvgPage),
    url('^avgpageone/$', MoniAvgPageOne),
    url('^curpage/$', MoniCurPage),
    url('^curpageone/$', MoniCurPageOne),
]