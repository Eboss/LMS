from django.conf.urls import patterns, include, url

from django.contrib import admin
from leaveform.views import *
admin.autodiscover()

urlpatterns = patterns('',
   
    url(r'^$', main),
    url(r'^login/',loginpage),
    
    url(r'^createaccount/',createaccount),
    url(r'^approverlogin/',approverlogin),
    url(r'^login_check/',login_check),
    url(r'^signup/',signup),
    url(r'^home/',home),
    url(r'^logout',logout_view),
    url(r'^leaveform/',leaveform)   ,
    url(r'^main/',main),
    url(r'^formdis/',formdis),
    url(r'^formdisplay/',formdisplay),
    url(r'^statusform/',statusform),
    url(r'^state/',state),
    url(r'^admin/', include(admin.site.urls)),
)
