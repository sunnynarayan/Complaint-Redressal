# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `#managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class Clink(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    cid = models.IntegerField(db_column='CID')  # Field name made lowercase.
    comid = models.IntegerField(db_column='ComID')  # Field name made lowercase.
    uid = models.IntegerField(db_column='UID')  # Field name made lowercase.
    time = models.DateTimeField()

    class Meta:
        #managed = False
        db_table = 'Clink'


class Com(models.Model):
    comid = models.IntegerField(db_column='comID', primary_key=True)  # Field name made lowercase.
    txt = models.TextField(db_column='Txt')  # Field name made lowercase.

    class Meta:
        #managed = False
        db_table = 'Com'


class Pollque(models.Model):
    pollid = models.IntegerField(db_column='PollID', primary_key=True)  # Field name made lowercase.
    uid = models.IntegerField(db_column='UID')  # Field name made lowercase.
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    ques = models.TextField()
    choice = models.TextField()
    choino = models.IntegerField(db_column='choiNo')  # Field name made lowercase.

    class Meta:
        #managed = False
        db_table = 'PollQue'


class Pollres(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    pollid = models.IntegerField(db_column='PollID')  # Field name made lowercase.
    uid = models.IntegerField(db_column='UID')  # Field name made lowercase.
    votetime = models.DateTimeField(db_column='voteTime')  # Field name made lowercase.
    choice = models.IntegerField()

    class Meta:
        #managed = False
        db_table = 'PollRes'


class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        #managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')

    class Meta:
        #managed = False
        db_table = 'auth_group_permissions'


class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)

    class Meta:
        #managed = False
        db_table = 'auth_permission'


class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
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
        #managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)

    class Meta:
        #managed = False
        db_table = 'auth_user_groups'


class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)

    class Meta:
        #managed = False
        db_table = 'auth_user_user_permissions'


class Complain(models.Model):
    cid = models.IntegerField(primary_key=True)
    uid = models.IntegerField(db_column='UID')  # Field name made lowercase.
    time = models.DateTimeField()
    hostel = models.IntegerField()
    type = models.IntegerField()
    subject = models.TextField()
    detail = models.TextField()
    history = models.TextField()
    comments = models.IntegerField()

    class Meta:
        #managed = False
        db_table = 'complain'


class Complainlink(models.Model):
    cid = models.IntegerField(db_column='CID')  # Field name made lowercase.
    studid = models.IntegerField(db_column='studID', blank=True, null=True)  # Field name made lowercase.
    secid = models.IntegerField(db_column='secID', blank=True, null=True)  # Field name made lowercase.
    woid = models.IntegerField(db_column='woID', blank=True, null=True)  # Field name made lowercase.
    wardenid = models.IntegerField(db_column='wardenID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        #managed = False
        db_table = 'complainLink'


class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.IntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    user = models.ForeignKey(AuthUser)

    class Meta:
        #managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        #managed = False
        db_table = 'django_content_type'


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        #managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        #managed = False
        db_table = 'django_session'


class Faculty(models.Model):
    fid = models.IntegerField(db_column='FID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=50)
    sex = models.CharField(max_length=1)
    mobile = models.CharField(max_length=10)
    off_ph = models.CharField(max_length=10)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=128)

    class Meta:
        #managed = False
        db_table = 'faculty'


class Hostel(models.Model):
    name = models.CharField(max_length=30)
    id = models.IntegerField(primary_key=True)  # AutoField?

    class Meta:
        #managed = False
        db_table = 'hostel'


class Secretary(models.Model):
    uid = models.IntegerField(db_column='UID', primary_key=True)  # Field name made lowercase.
    type = models.IntegerField()
    hostel = models.IntegerField()

    class Meta:
        #managed = False
        db_table = 'secretary'


class Student(models.Model):
    uid = models.IntegerField(db_column='UID', primary_key=True)  # Field name made lowercase.
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=128, blank=True)
    key_value = models.CharField(max_length=128, blank=True)
    name = models.CharField(max_length=100, blank=True)
    sex = models.CharField(max_length=1, blank=True)
    padd = models.TextField(blank=True)
    mobile = models.CharField(max_length=10, blank=True)
    email = models.CharField(max_length=50, blank=True)
    roll = models.CharField(max_length=8, blank=True)
    room = models.IntegerField(blank=True, null=True)
    hostel = models.IntegerField(blank=True, null=True)
    bloodgrp = models.CharField(db_column='bloodGrp', max_length=3, blank=True)  # Field name made lowercase.
    baccno = models.IntegerField(db_column='bAccNo', blank=True, null=True)  # Field name made lowercase.
    bank = models.CharField(max_length=50, blank=True)
    ifsc = models.CharField(db_column='IFSC', max_length=11, blank=True)  # Field name made lowercase.

    class Meta:
        #managed = False
        db_table = 'student'


class Warden(models.Model):
    fid = models.IntegerField(db_column='FID', primary_key=True)  # Field name made lowercase.
    hostel = models.IntegerField()

    class Meta:
        #managed = False
        db_table = 'warden'