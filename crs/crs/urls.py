from django.conf.urls import patterns, include, url
from django.contrib import admin
from user_module import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^crs/', 'user_module.views.login'),
    url(r'^login/$', 'user_module.views.afterLogin'),
    # url(r'^test/', 'user_module.views.ankt'),
    url(r'logout/$', 'user_module.views.logout'),
    url(r'^complainView/$', 'user_module.views.studentComplainView'),
    url(r'^lodgeComplain/$', 'user_module.views.studentLodgeComplain'),
	url(r'^studentHome/$', 'user_module.views.studentHome'),
    url(r'^studentProfile/$', 'user_module.views.studentProfile'),
    url(r'^studViewRate/$', 'user_module.views.studentViewRate'),
    url(r'^messrebate/$', 'user_module.views.studentMessRebate'),
    url(r'^studPoll/$', 'user_module.views.studentPoll'),
    url(r'^studHostelLeave/$', 'user_module.views.studentHolstelLeave'),
)
