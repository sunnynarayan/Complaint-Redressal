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
from django.core.urlresolvers import reverse
from django import forms

# global globlid
# globlid=0

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file'
    )

# def loadfile(request):
    # return render_to_response('list.html')

def isStudent(request):
    user_type = request.session.get("user_type", '')
    if user_type != "student":
        return False
    else:
        return True

def list(request): # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()
        return HttpResponse('uploaded')


            # Redirect to the document list after POST
            # return HttpResponseRedirect(reverse('crs.student.views.list'))
    # else:
        # form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    # documents = Document.objects.all()

    # Render list page with the documents and the form
    # return render_to_response(
    #     'list.html',
    #     {'documents': documents, 'form': form},
    #     context_instance=RequestContext(request)
    # )
    else:
        return HttpResponse('kjkj')

def loadPage(request):
    form =DocumentForm()
    return render_to_response('student/list.html',{'form': form})

def OpenHostelPage(request):
	username=request.session.get("username")
	obj=Student.objects.get(username=username)
	return render_to_response('student/HostelLeave.html',{'obj' : obj})

def HostelLeavingSubmit(request):
    laptop=request.POST.get('laptop', '')
    start_date=request.POST.get('start_date', datetime.datetime.now().date())
    end_date=request.POST.get('end_date' , datetime.datetime.now().date())
    destination=request.POST.get('destination', '')
    reason=request.POST.get('reason', '')
    username=request.session.get("username")
    obj = Student.objects.get(username=username)
    # rollno = obj.roll
    hostel=obj.hostel
    mobile=obj.mobile
    hostel = HostelLeavingInformation(name = obj.name,start_date =start_date, end_date = end_date,laptop=laptop,destination=destination,reason=reason,hostel=hostel,mobile=mobile)
    hostel.save()
    return HttpResponse('Hostel form submitted successfully')

def validatePassword(passwd):
    return ((len(passwd) < 21) and (len(passwd) > 7))


def studentComplainView(request):
    if not (isStudent(request)):
        return redirect('/crs/')
    uid = request.session.get('uid')
    qry = "SELECT a.status, a.cid, a.time, a.type, a.subject, a.comments, b.studID, @a:=@a+1 serial_number FROM complain a, complainLink b, (SELECT @a:= 0) AS a WHERE (b.studID = " + str(uid) + " OR b.studID = 0) AND a.cid = b.CID"
    serialComplainObjects = serialComplain.objects.raw(qry);
    # request.session['complains'] = serialComplainObjects;
    return render_to_response("student/viewStudComplain.html", {'list': serialComplainObjects});

# def viewrating(request):
# 	# hostel=request.session.get('hostel')
# 	sec=Secreatary.objects.get(hostel=1,type=2)
# 	return render_to_response('viewrating.html',{'sec':sec});

def studentViewComplain(request):
    index = request.GET.get('CID')
    qry = ""
    if request.session.get("user_type")=="student" :
        qry = "SELECT * FROM complain a, studComplainlink c WHERE c.cid = \'" + str(index) + "\' AND (c.studid = " + str(request.session.get('uid')) + " OR c.studid = 0)  AND c.cid = a.cid"        
    elif request.session.get("user_type")=="secretary" :
        qry = "SELECT * FROM complain a, complainLink b WHERE b.CID = \'" + str(index) + "\' AND (b.secid = " + str(request.session.get('uid')) + ") AND b.CID = a.cid"
    elif request.session.get("user_type")=="wardenOffice" :
        qry = "SELECT * FROM complain a, complainLink b WHERE b.CID = \'" + str(index) + "\' AND (b.woID = " + str(request.session.get('uid')) + ") AND b.CID = a.cid"
    elif request.session.get("user_type")=="warden" :
        qry = "SELECT * FROM complain a, complainLink b WHERE b.CID = \'" + str(index) + "\' AND (b.wardenID = " + str(request.session.get('uid')) + ") AND b.CID = a.cid"       
    complainObject = Complain.objects.raw(qry)
    # documents = Document.objects.get(id = (complainObject[0].picid))
    documents=Document.objects.get(cid=complainObject[0].cid)
    return render_to_response("student/compDetail.html", {'item': complainObject[0],'documents':documents})


def studentLodgeComplain(request):
    if not (isStudent(request)):
        return redirect('/crs/')
    form =DocumentForm()
    return render_to_response('student/studLodgeComplain.html',{'form': form})


def studentHome(request):
    if not (isStudent(request)):
        return redirect('/crs/')
    return render_to_response('student/studentHome.html');


def studentProfile(request):
    if not (isStudent(request)):
        return redirect('/crs/')
    return render_to_response('student/studentProfile.html');

def studEditProfile(request):
    uid=request.session.get('uid')
    obj=Student.objects.get(uid=uid)
    return render_to_response('student/studEditProfile.html',{'list' : obj})

def afterEditProfile(request):
    uid=request.session.get('uid');
    obj=Student.objects.get(uid=uid);
    padd=request.POST.get('padd')
    state=request.POST.get('state')
    city=request.POST.get('city')
    pincode=request.POST.get('pincode')
    bank=request.POST.get('bankName')
    ifsc=request.POST.get('ifsc')
    account=request.POST.get('accnum')
    email=request.POST.get('email')
    mobile=request.POST.get('mobile');
    if len(account)<=11 and  len(ifsc)<=11 and len(mobile)==10 and len(pincode)==6:
        obj.mobile=mobile;
        obj.bank=bank;
        obj.ifsc=ifsc;
        obj.baccno=account;
        obj.email=email
        obj.padd=padd
        obj.state=state
        obj.city=city
        obj.pincode=pincode
        obj.save();
        return render_to_response('student/studentHome.html')
    else:
        return HttpResponse(len(account))

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

def getComplainID(catagory, hostel):
	complain = ""
	if hostel == 1:
		complain = complain + "AS"
	elif hostel == 2:
		complain = complain + "AR"
	elif hostel == 3:
		complain = complain + "AR"
	else:
		complain = complain + "xx"

	complain = complain + "-"

	if catagory == 1:
		complain = complain + "ME"
	elif catagory == 2:
		complain = complain + "EN"
	elif catagory == 3:
		complain = complain + "TE"
	elif catagory == 4:
		complain = complain + "MA"
	else:
		complain = complain + "xx"

	complain = complain + "-"
	dt = datetime.datetime.now()
	dateComplain = dt.date()
	dateDatabase = Complainid.objects.get(hostel=hostel,type = catagory)
	if(dateDatabase.date < dateComplain):
		dateDatabase.date = dateComplain
		dateDatabase.id = 1
		dateDatabase.save()

	numericMonth = dt.month
	numericDay = dt.day
	numericYear = dt.year

	if numericDay < 10:
		complain = complain + "0" + str(numericDay)
	else:
		complain = complain + str(numericDay)

	complain = complain + "/"

	if numericMonth < 10:
		complain = complain + "0" + str(numericMonth)
	else:
		complain = complain + str(numericMonth)

	complain = complain + "/"
	numericYear = numericYear - 2000
	complain = complain + str(numericYear)
	compno = int(dateDatabase.id)
	dateDatabase.id = dateDatabase.id + 1
	dateDatabase.save()
	complain = complain + "-"
	if compno < 10:
		complain = complain + "000" + str(compno)
	elif compno < 100:
		complain = complain + "00" + str(compno)
	elif compno < 1000:
		complain = complain + "0" + str(compno)
	else:
		complain = complain + str(compno)
	
	return complain



def loadRateSecPage(request):
    return render_to_response('student/rateSec.html')

def rateSecretary(request):
    if not (isStudent(request)):
        return redirect('/crs/')
    uid = request.session.get('uid') 
    hostel=request.session.get('hostel')
    type1=request.POST.get('type')
    rating=request.POST.get('rating')
    type2=getCatagory(type1)
    obj=Secretary.objects.get(type=type2,hostel=hostel)
    secId=obj.uid
    try:
        secObj=Secretaryrating(secid=secId,rating=rating,studid=uid)
        secObj.save()
        count=0.0
        n=0.0
        finalRating=0.0
        # qry = "SELECT * FROM secretaryRating a WHERE a.secID = " + str(secId) 
        obj=Secretaryrating.objects.filter(secid =int(secId))
        for obje in obj:
            count +=obje.rating
            n=n+1
        finalRating=count/n
        sec=Secretary.objects.get(uid=secId)
        sec.rating=finalRating
        sec.save()
        return HttpResponse(sec.rating)
    except:
        return HttpResponse('You have already Voted')

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
    cid = getComplainID(catagory, hostel)
    complainObj = Complain(cid = cid, uid=uid, time=time, hostel=hostel, type=catagory, subject=subject, detail=detail, comments=0,
                           history=history, status = 1,picid = 0);
    complainObj.save();
    studComp1=Studcomplainlink(cid=cid,studid=uid)
    # studComp=Complainlink(cid=cid)
    studComp1.save()
    sec=Secretary.objects.get(type=catagory,hostel=hostel)
    warden=Warden.objects.get(hostel=hostel)
    studlink=Complainlink(cid=cid,studid=uid,secid=sec.uid,wardenid=warden.fid,woid=1025)
    studlink.save()
    
    # complain=Complain.objects.get(cid = cid)
    try:
    	newdoc=Document(docfile = request.FILES['docfile'],cid=cid)
    	# newdoc=Document.objects.get(docfile=request.FILES['docfile'])
    	newdoc.save()
    except:
    	d=request.POST['subject']
    try:
        first=request.POST.get('first')
        second=request.POST.get('second')
        third=request.POST.get('third')
        fourth=request.POST.get('fourth')
        fifth=request.POST.get('fifth')
        fid=Student.objects.get(roll = first).uid
        sid=Student.objects.get(roll = second).uid
        thirdid=Student.objects.get(roll= third).uid
        fourthid=Student.objects.get(roll = fourth).uid
        fifthid=Student.objects.get(roll = fifth).uid
        studComp1=Studcomplainlink(cid=cid,studid=fid)
        studComp2=Studcomplainlink(cid=cid,studid=sid)
        studComp3=Studcomplainlink(cid=cid,studid=thirdid)
        studComp4=Studcomplainlink(cid=cid,studid=fourthid)
        studComp5=Studcomplainlink(cid=cid,studid=fifthid)
        studComp1.save()
        studComp2.save()
        studComp3.save()
        studComp4.save()
        studComp5.save()
    except:
        d=request.POST['subject']
    secretaryObj = Secretary.objects.get(hostel=hostel, type=catagory)
    secid = secretaryObj.uid
    if (public == True):
        CLObj = Complainlink(cid=cid, studid=0, secid=secid)
        CLObj.save()
    else:
        CLObj = Complainlink(cid=cid, studid=uid, secid=secid)
        CLObj.save()
    return redirect('../complainView/');

def relodgeComplain(request):
	if not (isSecretary(request)):
		return redirect('/crs/')
	complainArray=request.POST.getlist('complain')
	length = len(complainArray)
	for x in range(0,length):
		comid = complainArray[x]
		obj=Complain.objects.get(cid=comid)
		if obj.status==1:
			obj.status=11
			obj.save()
		else:
			obj.status=22
			obj.save()
	# complainObj.wardenID = wardenID
	# complainObj.save()
	return redirect('../listComp/',{'msg':'Succesfully Redirected!!!'})
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
    state=student.state
    city=student.city
    pincode=student.pincode
    return render_to_response('student/studentProfile.html',
                              {'mobile': mobile, 'username': username, 'name': name, 'sex': sex, 'padd': padd,
                               'email': email, 'roll': roll, 'hostel': hostel, 'room': room, 'baccno': baccno,
                               'bank': bank, 'IFSC': IFSC,'state':state,'city':city,'pincode':pincode,'bloodgrp':bloodgrp});
