from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.http import *
from django.template import RequestContext, loader
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
import hashlib
import datetime
from login.models import *
import re


def isStudent(request):
    user_type = request.session.get("user_type", '')
    if user_type != "student":
        return False
    else:
        return True


def validatePassword(passwd):
    return ((len(passwd) < 21) and (len(passwd) > 7))


def studentComplainView(request):
    if not (isStudent(request)):
        return redirect('/crs/')
    uid = request.session.get('uid')
    qry = "SELECT a.cid, a.time, a.type, a.subject, a.comments, b.studID, @a:=@a+1 serial_number FROM complain a, complainLink b, (SELECT @a:= 0) AS a WHERE (b.studID = " + str(
        uid) + " OR b.studID = 0) AND a.cid = b.CID"
    serialComplainObjects = serialComplain.objects.raw(qry);
    # request.session['complains'] = serialComplainObjects;
    return render_to_response("student/viewStudComplain.html", {'list': serialComplainObjects});


def studentViewComplain(request):
    indexF = request.GET.get('CID')
    index = int(indexF)
    qry = "SELECT * FROM complain a, complainLink b WHERE b.CID = " + str(index) + " AND (b.studID = " + str(request.session.get('uid')) + " OR b.studID = 0 ) AND b.CID = a.cid"
    complainObject = Complain.objects.raw(qry)
    return render_to_response("student/compDetail.html", {'item': complainObject[0]})


def studentLodgeComplain(request):
    if not (isStudent(request)):
        return redirect('/crs/')
    return render_to_response('student/studLodgeComplain.html');


def studentHome(request):
    if not (isStudent(request)):
        return redirect('/crs/')
    return render_to_response('student/studentHome.html');


def studentProfile(request):
    if not (isStudent(request)):
        return redirect('/crs/')
    return render_to_response('student/studentProfile.html');


def studentViewRate(request):
    if not (isStudent(request)):
        return redirect('/crs/')
    return render_to_response('student/studViewRate.html');


def studentPoll(request):
    if not (isStudent(request)):
        return redirect('/crs/')
    return render_to_response('student/studPoll.html');


def studentHostelLeave(request):
    if not (isStudent(request)):
        return redirect('/crs/')
    return render_to_response('student/studHostelLeave.html');


def studentMessRebate(request):
    if not (isStudent(request)):
        return redirect('/crs/')
    return render_to_response('student/messrebate.html');


def getCatagory(str):
    if str == "Mess":
        return 1
    elif str == "Environment":
        return 2
    elif str == "Technical":
        return 3
    elif str == "Maintenance":
        return 4
    else:
        return 0


def message():
	return "The confirmation Link for the reset password is Confirmation Link.Please Click on it to reset password"

def getTypeDescription(code):
    if code == 1:
        return "Mess"
    elif code == 2:
        return "Environment"
    elif code == 3:
        return "Technical"
    elif code == 4:
        return "Maintenance"
    else:
        return "Other"


def lodgeComplainDetail(request):
    if not (isStudent(request)):
        return redirect('/crs/')
    subject = request.POST.get('subject');
    detail = request.POST.get('message');
    catagory = getCatagory(request.POST.get('catagory'));
    hostel = request.session.get("hostel");
    time = datetime.datetime.now();
    public = (request.POST.get('complainType') == "0");
    uid = request.session.get('uid');
    history = "Complain added by " + request.session.get("name") + " at time : " + str(time)
    complainObj = Complain(uid=uid, time=time, hostel=hostel, type=catagory, subject=subject, detail=detail, comments=0,
                           history=history);
    complainObj.save();
    secretaryObj = Secretary.objects.get(hostel=hostel, type=catagory)
    secid = secretaryObj.uid
    cid = (Complain.objects.get(uid=uid, time=time)).cid
    if (public == True):
        CLObj = Complainlink(cid=cid, studid=0, secid=secid)
        CLObj.save()
    else:
        CLObj = Complainlink(cid=cid, studid=uid, secid=secid)
        CLObj.save()
    return redirect('../complainView/');

# def forgetPassword(request):#forgetpassword page loading
# render_to_response(student/resetpassword.html)

# def resettingPassword(request):#resetting password
# newpassword=request.POST.get('password');
# uid=request.session.get('uid')
# if validatePassword(newpassword):
# student = Student.objects.get(uid=uid)
# hash_object = hashlib.sha256(b""+newpassword)
# passwd = hash_object.hexdigest()
# student.password=passwd
# student.save()
# render_to_response(student/studentHome.html)
# else:
# render_to_response(student/studentHome.html,{'msg':Invalid Password})


def studentProfile(request):
    if not (isStudent(request)):
        return redirect('/crs/')

    uid = request.session.get('uid')
    student = Student.objects.get(uid=uid)
    mobile = student.mobile
    username = student.username
    name = student.name
    sex = student.sex
    padd = student.padd
    email = student.email
    roll = student.roll
    room = student.room
    hostel = student.hostel
    bloodgrp = student.bloodgrp
    baccno = student.baccno
    bank = student.bank
    IFSC = student.ifsc
    return render_to_response('student/studentProfile.html',
                              {'mobile': mobile, 'username': username, 'name': name, 'sex': sex, 'padd': padd,
                               'email': email, 'roll': roll, 'hostel': hostel, 'room': room, 'baccno': baccno,
                               'bank': bank, 'IFSC': IFSC});
