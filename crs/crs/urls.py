from django.conf.urls import patterns, include, url
from django.contrib import admin
# from user_module import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^crs/', 'login.views.login'),
    #url(r'^captcha/', include('captcha.urls')),
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
    url(r'^studProfile/$', 'student.views.studentProfile'),
    url(r'^studHostelLeave/$', 'student.views.studentHostelLeave'),
    url(r'^lodgedComplainDetail/$', 'student.views.lodgeComplainDetail'),
    url(r'^listComp/$', 'secretary.views.secComplainView'),
    url(r'^listCompWardenOffice/$', 'wardenOffice.views.wardenOfficeComplainView'),
    url(r'^secComp/$', 'secretary.views.secLodgeComplain'),
    url(r'^wardenHome/$', 'warden.views.wardenHome'),
    url(r'^wardenViewComplain/$', 'warden.views.wardenComplainView'),
    url(r'^wardenViewSecretary/$', 'warden.views.viewSecretary'),
    url(r'^wardenEditProfile/$', 'warden.views.wardenEditProfile'),
    url(r'^forwardToWarden/$', 'secretary.views.forwardToWarden'),
    url(r'^wardenComplain/$', 'wardenOffice.views.wardenOfficeComplainView'),
    url(r'^forwardToWard/$', 'wardenOffice.views.forwardToWardenOffice'),
    url(r'^changePassword/$', 'login.views.changePasswd'),
    url(r'^restPassword/$', 'login.views.resetPasswd'),
    url(r'^mailTo/$', 'login.views.sendEmailForPassword'),
    url(r'^confirmationLink/$', 'login.views.forgetPassword'),
    url(r'^ForgetPasswordButton/$', 'login.views.onClickForgetPassword'),
    url(r'^newPassword/$', 'login.views.resettingPassword'),
    

   # url(r'^complainDetail/$', 'secretary.views.lodgeComplainDetail'),
)
