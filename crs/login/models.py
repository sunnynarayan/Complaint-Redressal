from __future__ import unicode_literals

from django.db import models
from django.db.models import FileField
from django.forms import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
 
class ContentTypeRestrictedFileField(models.FileField):
    content_types=['image/jpeg']
    max_upload_size=2121440
    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop("content_types")
        self.max_upload_size = kwargs.pop("max_upload_size")
        super(ContentTypeRestrictedFileField, self).__init__(*args, **kwargs)
 
    def clean(self, *args, **kwargs):
        data = super(ContentTypeRestrictedFileField, self).clean(*args, **kwargs)
        file = data.file
        try:
            content_type = file.content_type
            if content_type in self.content_types:
                if file.size > self.max_upload_size:
                    raise forms.ValidationError(_('Please keep filesize under'
                                                '%s. Current filesize %s')
                                                % (filesizeformat(self.max_upload_size), filesizeformat(file._size)))
            else:
                raise forms.ValidationError(_('Filetype not supported.'))
        except AttributeError:
            pass
 
        return data

class Comment(models.Model):
    commentid = models.IntegerField(db_column='commentId', primary_key=True)  # Field name made lowercase.
    cid = models.CharField(db_column='cid', max_length=19)
    name = models.CharField(max_length=100)
    time = models.DateTimeField()
    comment = models.TextField()

    class Meta:
        managed = False
        db_table = 'comment'


class Complain(models.Model):
    cid = models.CharField(primary_key=True, max_length=19)
    uid = models.IntegerField(db_column='UID')  # Field name made lowercase.
    time = models.DateTimeField()
    hostel = models.IntegerField(db_column='hostel')
    type = models.IntegerField()
    subject = models.TextField()
    detail = models.TextField()
    history = models.TextField()
    comments = models.IntegerField()
    status = models.IntegerField(blank=True, null=True)
    picid = models.CharField(db_column='picID', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'complain'
    def __str__(self):              # __unicode__ on Python 2
        return self.cid

class Complainid(models.Model):
    sno = models.IntegerField(primary_key=True)
    hostel = models.IntegerField(db_column='hostel')
    type = models.IntegerField()
    date = models.DateField()
    id = models.IntegerField(db_column='ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'complainID'


class Complainlink(models.Model):
    cid = models.CharField(db_column='CID', primary_key=True,max_length=19)  # Field name made lowercase.
    studid = models.IntegerField(db_column='studID', blank=True, null=True)  # Field name made lowercase.
    secid = models.IntegerField(db_column='secID', blank=True, null=True)  # Field name made lowercase.
    woid = models.IntegerField(db_column='woID', blank=True, null=True)  # Field name made lowercase.
    wardenid = models.IntegerField(db_column='wardenID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'complainLink'
    def __str__(self):              # __unicode__ on Python 2
        x = Complain.objects.get(cid=self.cid)
        return self.cid + " " + str(x.type)

class Document(models.Model):
    id = models.IntegerField(primary_key=True)
    docfile = models.ImageField(upload_to='documents/%Y/%m/%d')
    # docfile = models.FileField("Attachment", upload_to=path_and_rename("complaint_files", 'sales'), max_length=500,
                                # help_text="Browse a file")
    # docfile = models.CharField(max_length=100)
    cid = models.CharField(db_column='cid',max_length=19)

    class Meta:
        managed = False
        db_table = 'document'

class Faculty(models.Model):
    fid = models.IntegerField(db_column='FID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=50)
    sex = models.CharField(max_length=1)
    mobile = models.CharField(max_length=10)
    off_ph = models.CharField(max_length=10)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=128)
    key_value = models.CharField(max_length=4)
    email = models.CharField(max_length=50)
    iswarden = models.IntegerField(db_column='isWarden')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'faculty'
    def __str__(self):              # __unicode__ on Python 2
        return self.username + ' (' + self.name + ')'

class Fooditems(models.Model):
    fid = models.IntegerField(db_column='FID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(unique=True, max_length=100)
    vitamins = models.IntegerField()
    proteins = models.IntegerField()
    fat = models.IntegerField()
    nutritions = models.FloatField()

    class Meta:
        managed = False
        db_table = 'foodItems'
    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Hostel(models.Model):
    name = models.CharField(max_length=30)
    id = models.IntegerField(primary_key=True)  # AutoField?

    class Meta:
        managed = False
        db_table = 'hostel'


class HostelLeavingInformation(models.Model):
    sno = models.IntegerField(primary_key=True)
    studid = models.IntegerField(db_column='studid')
    start_date = models.DateTimeField(db_column='start_Date')  # Field name made lowercase.
    end_date = models.DateTimeField(db_column='end_Date')  # Field name made lowercase.
    destination = models.CharField(max_length=1000)
    reason = models.TextField()
    hostel = models.IntegerField(db_column='hostel')
    mobile = models.TextField()
    time = models.CharField(max_length=8)
    status = models.IntegerField()
    submittime = models.DateTimeField(db_column='submitTime')

    class Meta:
        managed = False
        db_table = 'hostel_leaving_information'
    def __str__(self):              # __unicode__ on Python 2
        stud = Student.objects.get(uid = self.studid)
        return stud.name

class Mealitems(models.Model):
    sno = models.IntegerField(primary_key=True)
    mid = models.IntegerField(db_column='MID')  # Field name made lowercase.
    fid = models.IntegerField(db_column='FID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mealItems'


class Meals(models.Model):
    mid = models.IntegerField(db_column='MID', primary_key=True)  # Field name made lowercase.
    items = models.IntegerField()
    fid = models.CharField(db_column='FID', unique=True, max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'meals'

    def __str__(self):              # __unicode__ on Python 2
        return str(self.mid) + " " + str(self.fid) + " " + str(self.items)

class Pollmenu(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    meal = models.TextField()
    hostel = models.IntegerField(db_column='hostel')
    type = models.IntegerField()
    protein = models.IntegerField()
    vitamin = models.IntegerField()
    fat = models.IntegerField()
    nutritions = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'pollMenu'

class Pollresult(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    hostel = models.IntegerField()
    type = models.IntegerField()
    meal = models.IntegerField()
    vote = models.IntegerField()
    protein = models.IntegerField()
    vitamin = models.IntegerField()
    fat = models.IntegerField()
    nutritions = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'pollResult'


class Pollvoting(models.Model):
    idx = models.IntegerField(primary_key=True)
    id = models.IntegerField(db_column='id')
    uid = models.IntegerField(db_column='UID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pollVoting'


class Secretary(models.Model):
    uid = models.IntegerField(db_column='UID', primary_key=True)  # Field name made lowercase.
    type = models.IntegerField()
    hostel = models.IntegerField(db_column='hostel')
    rating = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'secretary'
    
    def __str__(self):              # __unicode__ on Python 2
        stud = Student.objects.get(uid = self.uid)
        hostel = Hostel.objects.get(id=self.hostel)
        return stud.name + " (" + hostel.name +" - " +str(self.type) + ")"

class Secretaryrating(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    secid = models.IntegerField(db_column='secID')  # Field name made lowercase.
    studid = models.IntegerField(db_column='studID')  # Field name made lowercase.
    rating = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'secretaryRating'

    def __str__(self):              # __unicode__ on Python 2
        # sec = Secretary.objects.get(uid=self.secid)
        return str(self.id) + " secid = " + str(self.secid) + " studid = " + str(self.studid) + " rating = " + str(self.rating)

class Studcomplainlink(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    cid = models.CharField(db_column='cid', max_length=19)
    studid = models.IntegerField(db_column='studid')

    class Meta:
        managed = False
        db_table = 'studComplainlink'

    def __str__(self):              # __unicode__ on Python 2
        stud = Student.objects.get(uid=self.studid)
        return self.cid + " - " + str(stud.name)


class Student(models.Model):
    uid = models.IntegerField(db_column='UID', primary_key=True)  # Field name made lowercase.
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=128, blank=True)
    key_value = models.CharField(max_length=128, blank=True)
    name = models.CharField(max_length=100, blank=True)
    sex = models.CharField(max_length=1, blank=True)
    padd = models.TextField(blank=True)
    mobile = models.CharField(max_length=10, blank=True)
    email = models.CharField(max_length=50, blank=True)
    roll = models.CharField(max_length=8, blank=True)
    room = models.IntegerField(blank=True, null=True)
    hostel = models.IntegerField(db_column='hostel', blank=True, null=True)
    bloodgrp = models.CharField(db_column='bloodGrp', max_length=3, blank=True)  # Field name made lowercase.
    baccno = models.IntegerField(db_column='bAccNo')
    bank = models.CharField(max_length=50, blank=True)
    ifsc = models.CharField(db_column='IFSC', max_length=11, blank=True)  # Field name made lowercase.
    issec = models.IntegerField(db_column='isSec')  # Field name made lowercase.
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)

    class Meta:
        managed = False
        db_table = 'student'
    def __str__(self):              # __unicode__ on Python 2
        return self.username + " (" + self.name + ")"

class Warden(models.Model):
    fid = models.IntegerField(db_column='FID', primary_key=True)  # Field name made lowercase.
    hostel = models.IntegerField(db_column='hostel')

    class Meta:
        managed = False
        db_table = 'warden'
    def __str__(self):              # __unicode__ on Python 2
        fac = Faculty.objects.get(fid=self.fid)
        return fac.name