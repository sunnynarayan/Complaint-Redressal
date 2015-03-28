from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

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
    url(r'^crs/viewComplain/$', 'student.views.studentViewComplain'),
    url(r'^crs/lodgeComplain/$', 'student.views.studentLodgeComplain'),
	url(r'^crs/studentHome/$', 'student.views.studentHome'),
    url(r'^crs/studentProfile/$', 'student.views.studentProfile'),
    url(r'^crs/rateSecretary/$', 'student.views.rateSecretary'),
    url(r'^crs/messrebate/$', 'student.views.studentMessRebate'),
    url(r'^crs/studPoll/$', 'student.views.studentPoll'),
    url(r'^crs/studProfile/$', 'student.views.studentProfile'),
    url(r'^crs/studHostelLeave/$', 'student.views.studentHostelLeave'),
    url(r'^studEditProfile/$', 'student.views.studEditProfile'),
    url(r'^studAfterEditProfile/$', 'student.views.afterEditProfile'),
    url(r'^crs/lodgedComplainDetail/$', 'student.views.lodgeComplainDetail'),
    url(r'^crs/listComp/$', 'secretary.views.secComplainView'),
    url(r'^crs/listCompWardenOffice/$', 'wardenOffice.views.wardenOfficeComplainView'),
    url(r'^crs/secComp/$', 'secretary.views.secLodgeComplain'),
    url(r'^crs/wardenHome/$', 'warden.views.wardenHome'),
    url(r'^crs/wardenViewComplain/$', 'warden.views.wardenComplainView'),
    url(r'^crs/wardenViewSecretary/$', 'warden.views.viewSecretary'),
    url(r'^crs/wardenEditProfile/$', 'warden.views.wardenEditProfile'),
    url(r'^crs/forwardToWarden/$', 'secretary.views.forwardToWarden'),
    url(r'^crs/rejectComplain/$', 'secretary.views.rejectComplain'),
    url(r'^crs/wardenComplain/$', 'wardenOffice.views.wardenOfficeComplainView'),
    url(r'^crs/forwardToWard/$', 'wardenOffice.views.forwardToWardenOffice'),
    url(r'^crs/changePassword/$', 'login.views.changePasswd'),
    url(r'^crs/restPassword/$', 'login.views.resetPasswd'),
    url(r'^mailTo/$', 'login.views.sendEmailForPassword'),
    url(r'^confirmationLink/$', 'login.views.forgetPassword'),
    url(r'^ForgetPasswordButton/$', 'login.views.onClickForgetPassword'),
    url(r'^newPassword/$', 'login.views.resettingPassword'),
    url(r'^OpenHostelPage/$', 'student.views.OpenHostelPage'),
    url(r'^studHostelLeave/$', 'student.views.HostelLeavingSubmit'),
    url(r'^crs/poll/$', 'secretary.views.poll'),
    url(r'^crs/pollAddItem/$', 'secretary.views.pollAddItem'),
    url(r'^crs/pollViewItem/$', 'secretary.views.pollViewItem'),
    url(r'^crs/addingFoodItem/$', 'secretary.views.addingFoodItem'),
    url(r'^crs/pollMakeMeal/$', 'secretary.views.pollMakeMeal'),
    url(r'^crs/makingMeal/$', 'secretary.views.makingMeal'),
    url(r'^crs/loadRateSecPage/$','student.views.loadRateSecPage'),
    url(r'^studViewProfile/$','student.views.studentProfile'),
    url(r'^rateSecretary/$','student.views.rateSecretary'),
    url(r'^crs/viewMeal/$', 'secretary.views.viewMeal'),
    url(r'^crs/addItemToPoll/$', 'secretary.views.addItemToPoll'),
    url(r'^crs/viewPollOptions/$', 'secretary.views.viewPollOptions'),
    url(r'^crs/pdf/$', 'secretary.views.some_view'),
    url(r'^crs/list/$','student.views.list'),
    # url(r'^crs/viewrating/$','student.views.viewrating'),
    url(r'^Page/$','student.views.loadPage'),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


   # url(r'^complainDetail/$', 'secretary.views.lodgeComplainDetail'),

