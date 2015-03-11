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
    url(r'^listComp/$', 'secretary.views.secComplainView'),
    url(r'^secComp/$', 'secretary.views.secLodgeComplain'),
    url(r'^wardenHome/$', 'warden.views.wardenHome'),
    url(r'^wardenViewComplain/$', 'warden.views.wardenComplainView'),
    url(r'^wardenViewSecretary/$', 'warden.views.viewSecretary'),
    url(r'^wardenEditProfile/$', 'warden.views.wardenEditProfile'),
    url(r'^forwardToWarden/$', 'secretary.views.forwardToWarden'),
    

   # url(r'^complainDetail/$', 'secretary.views.lodgeComplainDetail'),
)
