from django.contrib import admin
from login.models import *
from secretary.models import *
from student.models import *
from warden.models import *
from wardenOffice.models import *

# admin.site.register(Clink)
# admin.site.register(Com)
# admin.site.register(Pollque)
# admin.site.register(Pollres)
# admin.site.register(AuthGroup)
# admin.site.register(AuthGroupPermissions)
# admin.site.register( AuthUserUserPermissions)
# admin.site.register(Complain)
# admin.site.register(Complainlink)
# admin.site.register(DjangoAdminLog)
# admin.site.register(DjangoContentType)
# admin.site.register(DjangoMigrations)
# admin.site.register(DjangoSession)
# admin.site.register(Faculty)
# admin.site.register(Hostel)
# admin.site.register(Secretary)
# admin.site.register(Student)
# admin.site.register(Warden)

admin.site.register(Comment)
admin.site.register(Document)
admin.site.register(Studcomplainlink)
admin.site.register(Complain)
admin.site.register(HostelLeavingInformation)
admin.site.register(Complainid)
admin.site.register(Complainlink)
admin.site.register(Fooditems)
admin.site.register(Meals)
admin.site.register(Pollmenu)
admin.site.register(Faculty)
admin.site.register(Hostel)
admin.site.register(Secretary)
admin.site.register(Student)
admin.site.register(Secretaryrating)
admin.site.register(Warden)