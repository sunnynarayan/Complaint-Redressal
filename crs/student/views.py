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
from datetime import timedelta
from django.db import transaction

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
	return render_to_response('student/HostelLeave.html',{'obj' : obj}, context_instance=RequestContext(request))

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
    return HttpResponse('Hostel Form submitted successfully')

def validatePassword(passwd):
    return ((len(passwd) < 21) and (len(passwd) > 7))


def studentComplainView(request):   #shows list of complains
    if not (isStudent(request)):
        return redirect('/crs/')
    uid = request.session.get('uid')
    qry = "SELECT a.status, a.cid, a.time, a.type, a.subject, a.comments FROM complain a, studComplainlink b WHERE (b.studid = " + str(uid) + " OR b.studid = 0) AND a.cid = b.cid"
    serialComplainObjects = Complain.objects.raw(qry);
    # request.session['complains'] = serialComplainObjects;
    #edited
    return render_to_response("student/tables.html", {'list': serialComplainObjects, 'msg': request.session.get('name')});

# def viewrating(request):
# 	# hostel=request.session.get('hostel')
# 	sec=Secreatary.objects.get(hostel=1,type=2)
# 	return render_to_response('viewrating.html',{'sec':sec});

def studentViewComplain(request):  #shows details of complain
    index = request.GET.get('CID')
    request.session['currentCid']=index;
    qry = ""
    if request.session.get("user_type")=="student" :
        qry = "SELECT * FROM complain a, studComplainlink c WHERE c.cid = \'" + str(index) + "\' AND (c.studid = " + str(request.session.get('uid')) + " OR c.studid = 0)  AND c.cid = a.cid"        
    elif request.session.get("user_type")=="secretary" :
        qry = "SELECT * FROM complain a, complainLink b WHERE b.CID = \'" + str(index) + "\' AND (b.secID = " + str(request.session.get('uid')) + ") AND b.CID = a.cid"
    elif request.session.get("user_type")=="wardenOffice" :
        qry = "SELECT * FROM complain a, complainLink b WHERE b.CID = \'" + str(index) + "\' AND (b.woID = " + str(request.session.get('uid')) + ") AND b.CID = a.cid"
    elif request.session.get("user_type")=="warden" :
        qry = "SELECT * FROM complain a, complainLink b WHERE b.CID = \'" + str(index) + "\' AND (b.wardenID = " + str(request.session.get('uid')) + ") AND b.CID = a.cid"       
    else :
        return HttpResponse('error')
    complainObject = Complain.objects.raw(qry)
    comment = []
    documents = []
    try:
    	documents.extend(Document.objects.get(cid=complainObject[0].cid))
    except:
        pass
    try:
        comment.extend(Comment.objects.filter(cid = complainObject[0].cid))
    except:
        pass
    return render_to_response("student/complainDetail.html", {'item': complainObject[0],'documents':documents,'comment':comment})

def studentLodgeComplain(request):
    if not (isStudent(request)):
        return redirect('/crs/')
    form =DocumentForm()
    return render_to_response('student/lodgeComp.html',{'form': form}, context_instance=RequestContext(request))


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
    return render_to_response('student/studEditProfile.html',{'list' : obj,'msg': request.session.get('name') })

def afterEditProfile(request):
    uid=request.session.get('uid');
    obj=Student.objects.get(uid=uid);
    padd=request.POST.get('padd')
    state=request.POST.get('state')
    city=request.POST.get('city')
    pincode=request.POST.get('pincode')
    bank=request.POST.get('bankName')
    ifsc=request.POST.get('ifsc')
    bgroup=request.POST.get('bgroup')
    account=request.POST.get('accnum')
    # email=request.POST.get('email')
    mobile=request.POST.get('mobile');
    if len(account)<=11 and  len(ifsc)<=11 and len(mobile)==10 and len(pincode)==6:
        obj.mobile=mobile;
        obj.bank=bank;
        obj.ifsc=ifsc;
        obj.baccno=account;
        # obj.email=email
        obj.padd=padd
        obj.state=state
        obj.city=city
        obj.pincode=pincode
        obj.bloodgrp=bgroup
        obj.save();
        # uid = request.session.get('uid')
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
                                   'bank': bank, 'IFSC': IFSC,'state':state,'city':city,'pincode':pincode,'bloodgrp':bloodgrp,'msg': name});
    else:
        return HttpResponse('Error')

# def rateSecretary(request):
#     if not (isStudent(request)):
#         return redirect('/crs/')
#     return render_to_response('student/rateSecretary.html');


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

@transaction.atomic
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
    uid=request.session.get('uid')
    obj=Student.objects.get(uid=uid)
    if obj.hostel==0:
        # qry="SELECT * FROM  secretary a WHERE a.hostel=\'" + "0" + "\'"
        # query="SELECT * FROM secretaryRating b WHERE b.studID = \'"+ str(uid) + "\'"
        secretary=Secretary.objects.filter(hostel = 0)
        request.session['secListForRating']=secretary;
        obj2 = None
        try:
            obj2=Secretaryrating.objects.filter(studid = uid)
            stud=[]
            for sec in secretary:
                stud.append(Student.objects.get(uid=sec.uid))
            return render_to_response('student/rateSecretaryAshoka.html',{'stud': stud,'sec' : secretary,'obj' : obj2})
        except:
            stud=[]
            for sec in secretary:
                stud.append(Student.objects.get(uid=sec.uid))
            return render_to_response('student/rateSecretaryAshoka.html',{'stud': stud,'sec' : secretary,'obj' : obj2})


        # return HttpResponse(obj2.rating)
        # try:
        #     return HttpResponse(obj2)
        # except:
        #     return HttpResponse('nkn')
        # stud=[]
        # for sec in secretary:
        #     stud.append(Student.objects.get(uid=sec.uid))
        # # return HttpResponse(stud[0].name)
        # return render_to_response('student/rateSecretaryAshoka.html',{'stud': stud,'sec' : secretary,'obj' : obj2})
    elif obj.hostel==1:
        qry="SELECT * FROM  secretary a WHERE a.hostel=\'" + "1" + "\'"
        secretary=Secretary.objects.raw(qry)
        stud=[]
        for sec in secretary:
            stud.append(Student.objects.get(uid=sec.uid))
        return render_to_response('student/rateSecretaryAshoka.html',{'secretary': stud})
        # return render_to_response('student/rateSecretaryAryabhatta.html')
    elif obj.hostel==2:
        qry="SELECT * FROM  secretary a WHERE a.hostel=\'" + "2" + "\'"
        secretary=Secretary.objects.raw(qry)
        stud=[]
        for sec in secretary:
            stud.append(Student.objects.get(uid=sec.uid))
        return render_to_response('student/rateSecretaryAshoka.html',{'secretary': stud,'sec':secretary})
        # return render_to_response('student/rateSecretaryChanakya1.html')
    elif obj.hostel==3:
        qry="SELECT * FROM  secretary a WHERE a.hostel=\'" + "3" + "\'"
        secretary=Secretary.objects.raw(qry)
        stud=[]
        for sec in secretary:
            stud.append(Student.objects.get(uid=sec.uid))
        return render_to_response('student/rateSecretaryAshoka.html',{'secretary': stud})
        # return render_to_response('student/rateSecretaryChanakya2.html')
    else :
        qry="SELECT * FROM  secretary a WHERE a.hostel=\'" + "4" + "\'"
        secretary=Secretary.objects.raw(qry)
        stud=[]
        for sec in secretary:
            stud.append(Student.objects.get(uid=sec.uid))
        return render_to_response('student/rateSecretaryAshoka.html',{'secretary': stud})
        # return render_to_response('student/rateSecretaryGBH.html')


def rateSecretary(request):
    if not (isStudent(request)):
        return redirect('/crs/')
    uid = request.session.get('uid') 
    count=0;
    ratingCount=0
    n=0
    finalRating=0.0
    lenn=0.0
    hostel=request.session.get('hostel')
    secList=request.session.get('secListForRating')
    # type1=request.POST.get('type')
    rating=request.POST.getlist('rating')
    length = len(rating)
    for eachSec in secList:
        secObj=Secretaryrating(secid=eachSec.uid,rating=rating[count],studid=uid)
        secObj.save()
        ++count
    for eachSec in secList:
        obj=Secretaryrating.objects.filter(secid = eachSec.uid)
        for obej in obj:
            ratingCount+=obej.rating
            n=n+1
        finalRating=ratingCount/n
        # lenn=finalRating
        # eachSec.rating=finalRating
        sec=Secretary.objects.get(uid=eachSec.uid)
        sec.rating=finalRating
        sec.save()
        ratingCount=0
        finalRating=0.0
        n=0
    return HttpResponse('Successfully Rated')

    # type2=getCatagory(type1)
    # obj=Secretary.objects.get(type=type2,hostel=hostel)
    # secId=obj.uid
    # try:
    #     secObj=Secretaryrating(secid=secId,rating=rating,studid=uid)
    #     secObj.save()
    #     count=0.0
    #     n=0.0
    #     finalRating=0.0
    #     obj=Secretaryrating.objects.filter(secid =int(secId))
    #     for obje in obj:
    #         count +=obje.rating
    #         n=n+1
    #     finalRating=count/n
    #     sec=Secretary.objects.get(uid=secId)
    #     sec.rating=finalRating
    #     sec.save()
    #     return HttpResponse(sec.rating)
    # except:
    #     return HttpResponse('You have already Voted')

def validateText(rawText):
    i = 0
    rawText = re.sub(r'[^a-zA-Z0-9\s,.:;\(\)\'"=\-+\/*#\<\>$&@%~?!\[\]\{\}\\]','',rawText)
    while i != len(rawText):
        ch = rawText[i]
        if re.search(r'[\'\\\<\>&!#";\-\/\*\{\}\(\)]', ""+ch):
            rawText = rawText[:i] + "&#" + str(ord(ch)) + ";" + rawText[i+1:]
            i = i + 3 + len(str(ord(ch)))
        else:
            i = i + 1
        # print str(i) + "," + str(len(rawText)) + " " + rawText
    return rawText

@transaction.atomic
def lodgeComplainDetail(request):
    if not (isStudent(request)):
        return redirect('/crs/')
    subject = request.POST.get('subject', '');
    subject = validateText(subject)
    detail = request.POST.get('message', '');
    detail = validateText(detail)
    if detail == '' or subject == '':
        return redirect('/crs/complainView/')
    catagory = getCatagory(request.POST.get('catagory'));
    hostel = request.session.get("hostel");
    time = (datetime.datetime.now() + timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d %H:%M:%S');
    complainAccess = int(request.POST.get('complainType'));
    uid = request.session.get('uid');
    history = "Complain added by " + request.session.get("name") + " at time : " + str(time)
    cid = getComplainID(catagory, hostel)
    complainObj = Complain(cid = cid, uid=uid, time=time, hostel=hostel, type=catagory, subject=subject, detail=detail, comments=0, history=history, status = 1);
    secretaryObj = Secretary.objects.get(hostel=hostel, type=catagory)
    secid = secretaryObj.uid
    try:
    	newdoc=Document(docfile = request.FILES['docfile'],cid=cid)
    	# newdoc=Document.objects.get(docfile=request.FILES['docfile'])
    	newdoc.save()
    except:
        pass

    SCLArray = []
    # CLArray = []
    CLObj = None
    if complainAccess == 2:
        # try:
        first=request.POST.get('first')
        second=request.POST.get('second','')
        third=request.POST.get('third','')
        fourth=request.POST.get('fourth','')
        fifth=request.POST.get('fifth','')
        rollArray = []
        rollArray.append(first)
        if not second == '':
            rollArray.append(second)
        if not third == '':
            rollArray.append(third)
        if not  fourth == '':
            rollArray.append(fourth)
        if not fifth == '':
            rollArray.append(fifth) 
        for x in rollArray:
            tempUid = Student.objects.get(roll = x).uid
            obj = Studcomplainlink(cid=cid,studid=tempUid)
            SCLArray.append(obj)

        CLObj = Complainlink(cid=cid, studid=uid, secid=secid)
        # except:
        #     pass
    elif complainAccess == 0:
        CLObj = Complainlink(cid=cid, studid=0, secid=secid)
    elif complainAccess == 1:
        CLObj = Complainlink(cid=cid, studid=uid, secid=secid)
    complainObj.save();
    CLObj.save()
    SCLObj = Studcomplainlink(cid=cid, studid=uid)
    SCLArray.append(SCLObj)
    for x in SCLArray:
        x.save()

    return redirect('/crs/complainView/');

def relodgeComplain(request):
	if not (isStudent(request)):
		return redirect('/crs/')
	comid=request.session.get('currentCid')
	obj=Complain.objects.get(cid=comid)
	if obj.status==1:
		obj.status=11
		obj.save()
	else:
		obj.status=22
		obj.save()
	# complainObj.wardenID = wardenID
	# complainObj.save()
	return redirect('/crs/complainView/',{'msg':'Succesfully Redirected!!!'})


def comment(request):
    if 'submit' in request.POST:
	   uid=request.session.get('uid')
	   user_type=request.session.get("user_type","")
	   comment=request.POST.get('cbox')
	   cid=request.session.get('currentCid')
	   time = (datetime.datetime.now() + timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d %H:%M:%S');	
	   if user_type == "student":
	       name=Student.objects.get(uid=uid).name
	       obj=Comment(cid=cid,comment=comment,time=time,name=name)
	       obj.save()
	       return redirect('/crs/complainView/')
	   elif user_type == "faculty":
	       name=Faculty.objects.get(fid=uid).name 
	       obj=Comment(cid=cid,comment=comment,time=time,name=name)
	       obj.save()
	       return redirect('/crs/complainView/')
	   else:
	       return HttpResponse('unsuccessfull')
    else:
        return HttpResponse('error')

def studentProfile(request):
    # if not (isStudent(request)):
    #     return redirect('/crs/')  //commented so that i can use in secretary

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
                               'bank': bank, 'IFSC': IFSC,'state':state,'city':city,'pincode':pincode,'bloodgrp':bloodgrp,'msg': name});
