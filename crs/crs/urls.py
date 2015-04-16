from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^crs/$', 'login.views.login'),
    # url(r'^captcha/', include('captcha.urls')),
    url(r'^crs/login/$', 'login.views.afterLogin'),
    # url(r'^test/', 'user_module.views.ankt'),
    url(r'crs/ApproveComplain/','login.views.ApproveComplain'),
    url(r'logout/','login.views.logout'),
    url(r'^crs/complainView/$', 'student.views.studentComplainView'),
    url(r'^comment/$', 'student.views.comment'),
    url(r'^crs/viewComplain/$', 'student.views.studentViewComplain'),
    url(r'^crs/lodgeComplain/$', 'student.views.studentLodgeComplain'),
	url(r'^crs/studentHome/$', 'student.views.studentHome'),
    url(r'^crs/studentProfile/$', 'student.views.studentProfile'),
    url(r'^crs/rateSecretary/$', 'student.views.rateSecretary'),
    url(r'^crs/messrebate/$', 'student.views.studentMessRebate'),
    url(r'^crs/studPoll/$', 'student.views.studentPoll'),
    url(r'^crs/studProfile/$', 'student.views.studentProfile'),
    url(r'^crs/studRelodge/$', 'student.views.relodgeComplain'),
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
    url(r'^crs/forwardToWardenOff/$', 'secretary.views.forwardToWardenOffice'),
    url(r'^crs/rejectComplain/$', 'secretary.views.rejectComplain'),
    url(r'^crs/wardenComplain/$', 'wardenOffice.views.wardenOfficeComplainView'),
    url(r'^crs/forwardToWard/$', 'wardenOffice.views.forwardToWarden'),
    url(r'^changePassword/$', 'login.views.changePasswd'),
    url(r'^crs/resetPassword/$', 'login.views.resetPasswd'),
    url(r'^mailTo/$', 'login.views.sendEmailForPassword'),
    url(r'^confirmationLink/([0-9a-z]{64})/$', 'login.views.forgetPassword'),
    url(r'^ForgetPasswordButton/$', 'login.views.onClickForgetPassword'),
    url(r'^newPassword/([0-9a-z]{64})/$', 'login.views.resettingPassword'),
    url(r'^OpenHostelPage/$', 'student.views.OpenHostelPage'),
    url(r'^submitHostelPage/$', 'student.views.HostelLeavingSubmit'),
    url(r'^viewPastForm/$', 'student.views.viewPastHostelLeaveForms'),
    url(r'^viewFormID/([0-9]+)/$', 'student.views.viewForm'),
    url(r'^rejectID/([0-9]+)/$', 'student.views.rejectForm'),
    url(r'^approveID/([0-9]+)/$', 'student.views.approveForm'),
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
    # url(r'^crs/viewPollOptions/$', 'secretary.views.viewPollOptions'),
    url(r'^crs/pdf/([0-9]+)/$', 'student.views.downloadPDF'),
    url(r'^crs/list/$','student.views.list'),
    # url(r'^crs/viewrating/$','student.views.viewrating'),
    url(r'^Page/$','student.views.loadPage'),
    url(r'^crs/search/$', 'secretary.views.searchDatabase'),
    url(r'^crs/searchResult/$', 'secretary.views.searchItem'),
    url(r'^crs/showComplain/([A-Za-z1-2]+)/([A-Za-z]+)/$','wardenOffice.views.showHostelWiseComplain'),
    # url(r'^crs/showComplain/([A-Za-z]+)/([A-Za-z]+)/$', 'warden.views.showHostelTypeWiseComplain'),
    url(r'^crs/showComplain/([A-Za-z1-2]+)/([A-Za-z]+)/([A-Za-z]+)/$','wardenOffice.views.showHostelAdUnadWiseComplain'),
    # url(r'^crs/getInfo([A-Za-z].)/$', 'warden.views.showHostelWiseInfo'),
    url(r'^crs/getSecInfo/([A-Za-z1-2]+)/$','wardenOffice.views.showHostelSecWiseInfo'),
    url(r'^crs/getStudInfo/([A-Za-z1-2]+)/$','wardenOffice.views.showHostelStudWiseInfo'),
    url(r'^crs/pollOptions/$', 'student.views.pollPage'),
    url(r'^crs/pollChoice/$', 'student.views.studentPolling'),
    url(r'^crs/pollResult/$', 'student.views.pollResult'),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



   # url(r'^complainDetail/$', 'secretary.views.lodgeComplainDetail'),

