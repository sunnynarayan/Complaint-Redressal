from django.conf.urls import patterns, include, url
from django.contrib import admin
# from user_module import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^crs/', 'login.views.login'),
    url(r'^login/$', 'login.views.afterLogin'),
    # url(r'^test/', 'user_module.views.ankt'),
    url(r'logout', 'login.views.logout'),
    url(r'^complainView/$', 'student.views.studentComplainView'),
    url(r'^lodgeComplain/$', 'student.views.studentLodgeComplain'),
	url(r'^studentHome/$', 'student.views.studentHome'),
    url(r'^studentProfile/$', 'student.views.studentProfile'),
    url(r'^studViewRate/$', 'student.views.studentViewRate'),
    url(r'^messrebate/$', 'student.views.studentMessRebate'),
    url(r'^studPoll/$', 'student.views.studentPoll'),
    url(r'^studHostelLeave/$', 'student.views.studentHostelLeave'),
    url(r'^lodgedComplainDetail/$', 'student.views.lodgeComplainDetail'),
)
