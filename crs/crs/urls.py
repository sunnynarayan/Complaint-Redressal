from django.conf.urls import patterns, include, url
from django.contrib import admin
# from user_module import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/$', include(admin.site.urls)),
    url(r'^crs/$', 'login.views.login'),
    # url(r'^captcha/', include('captcha.urls')),
    url(r'^crs/login/$', 'login.views.afterLogin'),
    # url(r'^test/', 'user_module.views.ankt'),
    url(r'logout', 'login.views.logout'),
    url(r'^crs/complainView/$', 'student.views.studentComplainView'),
    url(r'^crs/lodgeComplain/$', 'student.views.studentLodgeComplain'),
	url(r'^crs/studentHome/$', 'student.views.studentHome'),
    url(r'^crs/studentProfile/$', 'student.views.studentProfile'),
    url(r'^crs/studViewRate/$', 'student.views.studentViewRate'),
    url(r'^crs/messrebate/$', 'student.views.studentMessRebate'),
    url(r'^crs/studPoll/$', 'student.views.studentPoll'),
    url(r'^crs/studProfile/$', 'student.views.studentProfile'),
    url(r'^crs/studHostelLeave/$', 'student.views.studentHostelLeave'),
    url(r'^crs/lodgedComplainDetail/$', 'student.views.lodgeComplainDetail'),
    url(r'^crs/listComp/$', 'secretary.views.secComplainView'),
    url(r'^crs/listCompWardenOffice/$', 'wardenOffice.views.wardenOfficeComplainView'),
    url(r'^crs/secComp/$', 'secretary.views.secLodgeComplain'),
    url(r'^crs/wardenHome/$', 'warden.views.wardenHome'),
    url(r'^crs/wardenViewComplain/$', 'warden.views.wardenComplainView'),
    url(r'^crs/wardenViewSecretary/$', 'warden.views.viewSecretary'),
    url(r'^crs/wardenEditProfile/$', 'warden.views.wardenEditProfile'),
    url(r'^crs/forwardToWarden/$', 'secretary.views.forwardToWarden'),
    url(r'^crs/wardenComplain/$', 'wardenOffice.views.wardenOfficeComplainView'),
    url(r'^crs/forwardToWard/$', 'wardenOffice.views.forwardToWardenOffice'),
    url(r'^crs/changePassword/$', 'login.views.changePasswd'),
    url(r'^crs/restPassword/$', 'login.views.resetPasswd'),
    

   # url(r'^complainDetail/$', 'secretary.views.lodgeComplainDetail'),
)
