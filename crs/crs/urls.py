from django.conf.urls import patterns, include, url
from django.contrib import admin
from user_module import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^crs/', 'user_module.views.login'),
    url(r'^home/', 'user_module.views.afterLogin'),
    url(r'^test/', 'user_module.views.ankt'),

)
