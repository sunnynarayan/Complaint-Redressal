# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Clink(models.Model):
    cid = models.IntegerField(db_column='CID') # Field name made lowercase.
    comid = models.IntegerField(db_column='ComID') # Field name made lowercase.
    uid = models.IntegerField(db_column='UID') # Field name made lowercase.
    time = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'Clink'

class Com(models.Model):
    comid = models.IntegerField(db_column='comID', primary_key=True) # Field name made lowercase.
    txt = models.TextField(db_column='Txt') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'Com'

class Pollque(models.Model):
    pollid = models.IntegerField(db_column='PollID', primary_key=True) # Field name made lowercase.
    uid = models.IntegerField(db_column='UID') # Field name made lowercase.
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    ques = models.TextField()
    choice = models.TextField()
    choino = models.IntegerField(db_column='choiNo') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'PollQue'

class Pollres(models.Model):
    pollid = models.IntegerField(db_column='PollID') # Field name made lowercase.
    uid = models.IntegerField(db_column='UID') # Field name made lowercase.
    votetime = models.DateTimeField(db_column='voteTime') # Field name made lowercase.
    choice = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'PollRes'

class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=80)
    class Meta:
        managed = False
        db_table = 'auth_group'

class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')
    class Meta:
        managed = False
        db_table = 'auth_group_permissions'

class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'auth_permission'

class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'auth_user'

class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)
    class Meta:
        managed = False
        db_table = 'auth_user_groups'

class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)
    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'

class Complain(models.Model):
    cid = models.IntegerField(primary_key=True)
    uid = models.IntegerField(db_column='UID') # Field name made lowercase.
    time = models.DateTimeField()
    hostel = models.IntegerField()
    type = models.IntegerField()
    subject = models.TextField()
    detail = models.TextField()
    comment = models.TextField()
    sid = models.IntegerField()
    bypass = models.CharField(max_length=1)
    class Meta:
        managed = False
        db_table = 'complain'

class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)
    action_time = models.DateTimeField()
    user = models.ForeignKey(AuthUser)
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.IntegerField()
    change_message = models.TextField()
    class Meta:
        managed = False
        db_table = 'django_admin_log'

class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'django_content_type'

class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'django_session'

class Faculty(models.Model):
    uid = models.IntegerField(db_column='UID', unique=True) # Field name made lowercase.
    name = models.CharField(max_length=50)
    sex = models.CharField(max_length=1)
    mobile = models.CharField(max_length=10)
    off_ph = models.CharField(max_length=10)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=128, blank=True)
    class Meta:
        managed = False
        db_table = 'faculty'

class Hostel(models.Model):
    name = models.CharField(max_length=30)
    id = models.IntegerField(primary_key=True)
    class Meta:
        managed = False
        db_table = 'hostel'

class Secretary(models.Model):
    uid = models.IntegerField(db_column='UID') # Field name made lowercase.
    sid = models.IntegerField(db_column='SID', primary_key=True) # Field name made lowercase.
    type = models.IntegerField()
    hostel = models.IntegerField()
    designation = models.CharField(max_length=20)
    class Meta:
        managed = False
        db_table = 'secretary'

class Student(models.Model):
    uid = models.IntegerField(db_column='UID', primary_key=True) # Field name made lowercase.
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=128, blank=True)
    key_value = models.CharField(max_length=128, blank=True)
    name = models.CharField(max_length=100)
    sex = models.CharField(max_length=1)
    padd = models.TextField()
    mobile = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    roll = models.CharField(max_length=8)
    room = models.IntegerField()
    hostel = models.IntegerField()
    bloodgrp = models.CharField(db_column='bloodGrp', max_length=3) # Field name made lowercase.
    baccno = models.IntegerField(db_column='bAccNo', blank=True, null=True) # Field name made lowercase.
    bank = models.CharField(max_length=50, blank=True)
    ifsc = models.CharField(db_column='IFSC', max_length=11, blank=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'student'

class Warden(models.Model):
    uid = models.ForeignKey(Faculty, db_column='UID') # Field name made lowercase.
    hostel = models.ForeignKey(Hostel, db_column='hostel')
    class Meta:
        managed = False
        db_table = 'warden'

