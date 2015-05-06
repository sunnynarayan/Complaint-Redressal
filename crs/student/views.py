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
from wardenOffice.views import *
# from warden.views import *
# from secretary.views import *
from django.core.files import File
from reportlab.pdfgen import canvas
from reportlab.platypus import Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import landscape
import os, inspect

def secViewComplain(complainObject):
    comment = []
    documents = []
    try:
        documents=(Document.objects.get(cid=complainObject[0].cid))
    except:
        pass
    try:
        comment.extend(Comment.objects.filter(cid = complainObject[0].cid))
    except:
        pass
    return render_to_response("secretary/complainDetail.html", {'item': complainObject[0],'documents':documents,'comment':comment})
    
def isWarden(request):
    user_type = request.session.get("user_type",'')
    if user_type != "warden":
        return False
    else:
        return True

class MealItems:
    def __init__(self , MID):
        self.mid = MID
        self.FoodItems = []
        self.protein = 0
        self.vitamin = 0
        self.fat = 0
        self.PopulateFid()
        self.avgnutrition = int((self.fat + self.protein + self.fat)/3)
        self.name = ""
        for fobj in self.FoodItems:
            self.name = self.name + fobj.name + ","

    def PopulateFid(self):
        mealItems = Mealitems.objects.filter(mid = self.mid)
        for mi in mealItems:
            fitem = Fooditems.objects.get(fid=mi.fid)
            self.FoodItems.append(fitem)
            self.protein = self.protein + fitem.proteins
            self.vitamin = self.vitamin + fitem.vitamins
            self.fat = self.fat + fitem.fat
        self.protein = int(self.protein/len(mealItems))
        self.vitamin = int(self.vitamin/len(mealItems))
        self.fat = int(self.fat /len(mealItems))

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file'
    )

def finalPollResult(request):
    totalpollresults = Pollresult.objects.filter(hostel=request.session.get('hostel')).count()
    if totalpollresults <= 0:
        return HttpResponse("Sorry no poll results are available!")
    breakfastPollOptions = []
    lunchPollOptions = []
    dinnerPollOptions = []
    dataB = ""
    dataL = ""
    dataD = ""
    b = 1
    l = 1
    d = 1
    try:
        breakfastPollOptions.extend(Pollresult.objects.filter(hostel=request.session.get('hostel')).filter(type = 1))
    except:
        pass
    try:
        lunchPollOptions.extend(Pollresult.objects.filter(hostel=request.session.get('hostel')).filter(type = 2))
    except:
        pass
    try:
        dinnerPollOptions.extend(Pollresult.objects.filter(hostel=request.session.get('hostel')).filter(type = 3))
    except:
        pass
    for x in breakfastPollOptions:
        dataB = dataB + "B-Item " + str(b) + "\t" + str(x.vote) + "\n"
        b = b + 1
    for x in lunchPollOptions:
        dataL = dataL + "L-Item " + str(l) + "\t" + str(x.vote) + "\n"
        l = l + 1
    for x in dinnerPollOptions:
        dataD = dataD + "D-Item " + str(d) + "\t" + str(x.vote) + "\n"
        d = d + 1
        
    with open('/mnt/edu/Software/Complaint-Redressal/Complaint-Redressal/crs/student/static/FinalVotingDataB.tsv', 'w') as f:
        myfile = File(f)
        myfile.write("meal\tvotes\n"+dataB)
    with open('/mnt/edu/Software/Complaint-Redressal/Complaint-Redressal/crs/student/static/FinalVotingDataL.tsv', 'w') as f:
        myfile = File(f)
        myfile.write("meal\tvotes\n"+dataL)
    with open('/mnt/edu/Software/Complaint-Redressal/Complaint-Redressal/crs/student/static/FinalVotingDataD.tsv', 'w') as f:
        myfile = File(f)
        myfile.write("meal\tvotes\n"+dataD)

    return render_to_response("student/pollResult.html", {'list1' : breakfastPollOptions, 'list2' : lunchPollOptions, 'list3' : dinnerPollOptions })

def isStudent(request):
    user_type = request.session.get("user_type", '')
    if user_type != "student":
        return False
    else:
        return True
def isSecretary(request):
    user_type = request.session.get("user_type",'')
    if user_type != "secretary":
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
        return HttpResponse('Error!!')

def loadPage(request):
    form =DocumentForm()
    return render_to_response('student/list.html',{'form': form, 'msg': request.session.get('name')})


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
    currDate = datetime.datetime.now()
    if request.session.get("user_type")=="student" :
        qry = "SELECT * FROM complain a, studComplainlink c WHERE c.cid = \'" + str(index) + "\' AND (c.studid = " + str(request.session.get('uid')) + " OR c.studid = 0)  AND c.cid = a.cid"
        complainObject = Complain.objects.raw(qry)
        comment = []
        documents = []
        s1 = str(complainObject[0].time)
        complainTime=int(datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),int(s1[11:13]),int(s1[14:16]),int(s1[17:19])).strftime('%s'))
        diff = (int(datetime.datetime.now().strftime('%s'))) - complainTime + 19800 
        # return HttpResponse(complainObject[0].access) 
        try:
            documents=(Document.objects.get(cid=complainObject[0].cid))
        except:
            pass
        try:
            comment.extend(Comment.objects.filter(cid = complainObject[0].cid))
        except:
            pass
        return render_to_response("student/complainDetail.html", {'item': complainObject[0],'documents':documents,'comment':comment, 'diff' : diff, 'msg': request.session.get('name')})        
    elif request.session.get("user_type")=="secretary" :
        qry = "SELECT * FROM complain a, complainLink b WHERE b.CID = \'" + str(index) + "\' AND (b.secID = " + str(request.session.get('uid')) + ") AND b.CID = a.cid"
        complainObject = Complain.objects.raw(qry)
        return secViewComplain(complainObject)
        
    elif request.session.get("user_type")=="wardenOffice" :
        qry = "SELECT * FROM complain a, complainLink b WHERE b.CID = \'" + str(index) + "\' AND (b.woID = " + str(request.session.get('uid')) + ") AND b.CID = a.cid"
        complainObject = Complain.objects.raw(qry)
        return wardenOfficeViewComplain(complainObject)
    elif request.session.get("user_type")=="warden" :
        qry = "SELECT * FROM complain a, complainLink b WHERE b.CID = \'" + str(index) + "\' AND (b.wardenID = " + str(request.session.get('uid')) + ") AND b.CID = a.cid"
        complainObject = Complain.objects.raw(qry)
        return wardenViewComplain(complainObject)      
    else :
        return HttpResponse('error')
    

def studentLodgeComplain(request):
    if not (isStudent(request)):
        return redirect('/crs/')
    form =DocumentForm()
    msg=request.session.get('username')
    message=""
    return render_to_response('student/lodgeComp.html',{'msg2':message,'form': form},context_instance=RequestContext(request))
def studentHome(request):
    if not (isStudent(request)):
        return redirect('/crs/')
    return render_to_response('student/studentHome.html',{'msg': request.session.get('name')});


def studentProfile(request):
    if isStudent(request):
        # return redirect('/crs/')
        return render_to_response('student/studentProfile.html');
    elif isSecretary(request):
        return render_to_response('secretary/viewProfile.html')
    else:
        return redirect('/crs/')

def studEditProfile(request):
    if isStudent(request):
        uid=request.session.get('uid')
        obj=Student.objects.get(uid=uid)
        return render_to_response('student/studEditProfile.html',{'list' : obj,'msg': request.session.get('name') })
    elif isSecretary(request):
        uid=request.session.get('uid')
        obj=Student.objects.get(uid=uid)
        return render_to_response('secretary/EditProfile.html',{'list' : obj,'msg': request.session.get('name') })
    else:
        return redirect('/crs/')

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
    if len(account)==11 and  len(ifsc)==11 and len(mobile)==10 and len(pincode)==6:
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
        return render_to_response('student/studentProfile.html',
                                  {'mobile': mobile, 'username': username, 'name': name, 'sex': sex, 'padd': padd,
                                   'email': email, 'roll': roll, 'hostel': hostel, 'room': room, 'baccno': baccno,
                                   'bank': bank, 'IFSC': IFSC,'state':state,'city':city,'pincode':pincode,'bloodgrp':bloodgrp,'msg': name});
    elif isSecretary(request):
        message="Invalid Input"
        return render_to_response('secretary/EditProfile.html',{'list' : obj,'msg2':message,'msg': request.session.get('name') })
    else:
        message="Invalid Input"
        return render_to_response('student/studEditProfile.html',{'list' : obj,'msg2':message,'msg':request.session.get('name')})

# def rateSecretary(request):
#     if not (isStudent(request)):
#         return redirect('/crs/')
#     return render_to_response('student/rateSecretary.html');


def studentPoll(request):
    if not (isStudent(request)):
        return redirect('/crs/')
    return render_to_response('student/studPoll.html', {'msg': request.session.get('name')});


def studentHostelLeave(request):
    if not (isStudent(request)):
        return redirect('/crs/')
    return render_to_response('student/studHostelLeave.html', {'msg': request.session.get('name')});


def studentMessRebate(request):
    if not (isStudent(request)):
        return redirect('/crs/')
    return render_to_response('student/messrebate.html', {'msg': request.session.get('name')});


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
            return render_to_response('student/rateSecretaryAshoka.html',{'stud': stud,'sec' : secretary,'obj' : obj2, 'msg': request.session.get('name')})
        except:
            stud=[]
            for sec in secretary:
                stud.append(Student.objects.get(uid=sec.uid))
            return render_to_response('student/rateSecretaryAshoka.html',{'stud': stud,'sec' : secretary,'obj' : obj2, 'msg': request.session.get('name')})


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
        # qry="SELECT * FROM  secretary a WHERE a.hostel=\'" + "1" + "\'"
        secretary=Secretary.objects.filter(hostel=1)
        request.session['secListForRating']=secretary;
        obj2 = None
        try:
            obj2=Secretaryrating.objects.filter(studid = uid)
            stud=[]
            for sec in secretary:
                stud.append(Student.objects.get(uid=sec.uid))
            return render_to_response('student/rateSecretaryAshoka.html',{'stud': stud,'sec' : secretary,'obj' : obj2, 'msg': request.session.get('name')})
        except:
            stud=[]
            for sec in secretary:
                stud.append(Student.objects.get(uid=sec.uid))
            return render_to_response('student/rateSecretaryAshoka.html',{'stud': stud,'sec' : secretary,'obj' : obj2, 'msg': request.session.get('name')})
        # stud=[]
        # for sec in secretary:
        #     stud.append(Student.objects.get(uid=sec.uid))
        # return render_to_response('student/rateSecretaryAshoka.html',{'secretary': stud})
        # return render_to_response('student/rateSecretaryAryabhatta.html')
    elif obj.hostel==2:
        qry="SELECT * FROM  secretary a WHERE a.hostel=\'" + "2" + "\'"
        secretary=Secretary.objects.filter(hostel=2)
        request.session['secListForRating']=secretary;
        obj2 = None
        try:
            obj2=Secretaryrating.objects.filter(studid = uid)
            stud=[]
            for sec in secretary:
                stud.append(Student.objects.get(uid=sec.uid))
            return render_to_response('student/rateSecretaryAshoka.html',{'stud': stud,'sec' : secretary,'obj' : obj2, 'msg': request.session.get('name')})
        except:
            stud=[]
            for sec in secretary:
                stud.append(Student.objects.get(uid=sec.uid))
            return render_to_response('student/rateSecretaryAshoka.html',{'stud': stud,'sec' : secretary,'obj' : obj2, 'msg': request.session.get('name')})
        # stud=[]
        # for sec in secretary:
        #     stud.append(Student.objects.get(uid=sec.uid))
        # return render_to_response('student/rateSecretaryChanakya1.html',{'secretary': stud,'sec':secretary})
        # # return render_to_response('student/rateSecretaryChanakya1.html')
    elif obj.hostel==3:
        # qry="SELECT * FROM  secretary a WHERE a.hostel=\'" + "3" + "\'"
        secretary=Secretary.objects.filter(hostel=3)
        request.session['secListForRating']=secretary;
        obj2 = None
        try:
            obj2=Secretaryrating.objects.filter(studid = uid)
            stud=[]
            for sec in secretary:
                stud.append(Student.objects.get(uid=sec.uid))
            return render_to_response('student/rateSecretaryAshoka.html',{'stud': stud,'sec' : secretary,'obj' : obj2, 'msg': request.session.get('name')})
        except:
            stud=[]
            for sec in secretary:
                stud.append(Student.objects.get(uid=sec.uid))
            return render_to_response('student/rateSecretaryAshoka.html',{'stud': stud,'sec' : secretary,'obj' : obj2, 'msg': request.session.get('name')})
        # stud=[]
        # for sec in secretary:
        #     stud.append(Student.objects.get(uid=sec.uid))
        # return render_to_response('student/rateSecretaryAshoka.html',{'secretary': stud})
        # # return render_to_response('student/rateSecretaryChanakya2.html')
    else :
        # qry="SELECT * FROM  secretary a WHERE a.hostel=\'" + "4" + "\'"
        secretary=Secretary.objects.filter(hostel=4)
        request.session['secListForRating']=secretary;
        obj2 = None
        try:
            obj2=Secretaryrating.objects.filter(studid = uid)
            stud=[]
            for sec in secretary:
                stud.append(Student.objects.get(uid=sec.uid))
            return render_to_response('student/rateSecretaryAshoka.html',{'stud': stud,'sec' : secretary,'obj' : obj2, 'msg': request.session.get('name')})
        except:
            stud=[]
            for sec in secretary:
                stud.append(Student.objects.get(uid=sec.uid))
            return render_to_response('student/rateSecretaryAshoka.html',{'stud': stud,'sec' : secretary,'obj' : obj2, 'msg': request.session.get('name')})
        # stud=[]
        # for sec in secretary:
        #     stud.append(Student.objects.get(uid=sec.uid))
        # return render_to_response('student/rateSecretaryAshoka.html',{'secretary': stud})
        # # return render_to_response('student/rateSecretaryGBH.html')


def rateSecretary(request):
    if not (isStudent(request)):
        return redirect('/crs/')
    uid = request.session.get('uid') 
    count=0;
    ratingCount=0.0
    n=0
    finalRating=0.0
    lenn=0
    hostel=request.session.get('hostel')
    secList=request.session.get('secListForRating')
    # type1=request.POST.get('type')
    rating=request.POST.getlist('rating')
    length = len(rating)
    for eachSec in secList:
        try:
            ob=Secretaryrating.objects.get(secid=eachSec.uid,studid=uid)
            ob.rating=rating[count]
            count=count+1
            ob.save()
        except:
            secObj=Secretaryrating(secid=eachSec.uid,rating=rating[count],studid=uid)
            secObj.save()
            ++count
    for eachSec in secList:
        obj=Secretaryrating.objects.filter(secid = eachSec.uid)
        for obej in obj:
            ratingCount=ratingCount+obej.rating
            n=n+1
        finalRating=ratingCount/n
        # return HttpResponse(finalRating)
        sec=Secretary.objects.get(uid=eachSec.uid)
        sec.rating=finalRating
        # return HttpResponse(finalRating)
        sec.save()
        # return HttpResponse(finalRating)
        # return HttpResponse(finalRating)
        ratingCount=0.0
        finalRating=0.0
        n=0
    return redirect('/crs/complainView/');

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
def validateRoll(roll):
    rawText = re.sub(r'^\d\d\d\d[A-Z][A-Z]\d\d$','',rawText)
    if len(rawText) == 0:
        return roll
    else:
        return ''
@transaction.atomic
def lodgeComplainDetail(request):
    if not (isStudent(request)):
        return redirect('/crs/')
    subject = request.POST.get('subject');
    subject = validateText(subject)
    detail = request.POST.get('message');
    detail = validateText(detail)
    if detail == '' or subject == '':
        return redirect('/crs/complainView/')
    catagory = getCatagory(request.POST.get('catagory'));
    hostel = request.session.get('hostel');
    time = (datetime.datetime.now() + timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d %H:%M:%S');
    complainAccess = int(request.POST.get('complainType'));
    # return HttpResponse(complainAccess)
    uid = request.session.get('uid');
    history = "Complain added by " + request.session.get("name") + " at time : " + str(time)
    cid = getComplainID(catagory,int(hostel))
    complainObj = Complain(cid = cid, uid=uid,time=time, hostel=hostel , type=catagory, subject=subject,detail=detail, comments=0, history=history, status = 1);
    complainObj.save()
    secretaryObj = Secretary.objects.get(hostel=hostel,type=catagory)
    secid = secretaryObj.uid
    SCLArray = []
    # CLArray = []
    CLObj = None
    if complainAccess == 2:
        complinObj=Complain.objects.get(cid=cid)
        # complainObj.access = 2
        # try:

        # first=validateRoll(request.POST.get('first').upper())
        # second=validateRoll(request.POST.get('second','').upper())
        # third=validateRoll(request.POST.get('third','').upper())
        # fourth=validateRoll(request.POST.get('fourth','').upper())
        # fifth=validateRoll(request.POST.get('fifth','').upper())

        first=request.POST.get('first').upper()
        # return HttpResponse(first)
        second=request.POST.get('second','').upper()
        third=request.POST.get('third','').upper()
        fourth=request.POST.get('fourth','').upper()
        fifth=request.POST.get('fifth','').upper()
        user_roll=Student.objects.get(uid=uid).roll
        if first == user_roll or  second == user_roll or third==user_roll or fourth==user_roll or fifth==user_roll or len(first)==0:
            form =DocumentForm()
            msg=request.session.get('username')
            message = "You can't enter your own roll number"
            return render_to_response('student/lodgeComp.html',{'msg2':message,'msg':msg,'form': form},context_instance=RequestContext(request))
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
            try:
                tempUid = Student.objects.get(roll = x).uid
                obj = Studcomplainlink(cid=cid,studid=tempUid)
                SCLArray.append(obj)
            except:
                pass
        CLObj = Complainlink(cid=cid, studid=uid, secid=secid)
        # except:
        #     pass
    elif complainAccess == 0:
        complinObj=Complain.objects.get(cid=cid)
        # complainObj.access = 0
        CLObj = Complainlink(cid=cid, studid=0, secid=secid)
    elif complainAccess == 1:
        complinObj=Complain.objects.get(cid=cid)
        # complainObj.access = 1
        CLObj = Complainlink(cid=cid, studid=uid, secid=secid)
    complainObj.save()
    CLObj.save()
    SCLObj = Studcomplainlink(cid=cid, studid=uid)
    SCLArray.append(SCLObj)
    for x in SCLArray:
        x.save()
    try:
        newdoc=Document(docfile =request.FILES['docfile'],cid=cid)
        # im = Image.open(newdoc)
        # if im.format not in ('BMP', 'PNG', 'JPEG'):
        #     return HttpResponse('Invalid File Format')
        # # newdoc=Document.objects.get(docfile=request.FILES['docfile'])
        newdoc.save()
    except:
        pass

    # return HttpResponse("451")
    return redirect('/crs/complainView/');

def relodgeComplain(request):
	if not (isStudent(request)):
		return redirect('/crs/')
	comid=request.session.get('currentCid')
	obj=Complain.objects.get(cid=comid)
	if obj.status==10:
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
	   comment=validateText(request.POST.get('cbox'))
	   cid=request.session.get('currentCid')
	   time = (datetime.datetime.now() + timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d %H:%M:%S');	
	   if user_type == "student" and len(comment)!=0:
	       name=Student.objects.get(uid=uid).name
	       obj=Comment(cid=cid,comment=comment,time=time,name=name)
	       obj.save()
	       return redirect('/crs/complainView/')
	   elif user_type == "faculty" and len(comment)!=0:
	       name=Faculty.objects.get(fid=uid).name 
	       obj=Comment(cid=cid,comment=comment,time=time,name=name)
	       obj.save()
	       return redirect('/crs/complainView/')
	   else:
	       return HttpResponse('Comment cant be empty')
    else:
        return HttpResponse('error')

def studentProfile(request):
    # if not (isStudent(request)):
    #     return redirect('/crs/')  //commented so that i can use in secretary
    if not (isStudent(request) or isSecretary(request)):
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
    address = ""
    if isStudent(request):
        address = "student/studentProfile.html"
    else:
        address = "secretary/viewProfile.html"
    return render_to_response(address,
                              {'mobile': mobile, 'username': username, 'name': name, 'sex': sex, 'padd': padd,
                               'email': email, 'roll': roll, 'hostel': hostel, 'room': room, 'baccno': baccno,
                               'bank': bank, 'IFSC': IFSC,'state':state,'city':city,'pincode':pincode,'bloodgrp':bloodgrp,'msg': name});

def checkAvailabilityOfPoll(hostel):
    #if PollMenu contain any entry of this hostel then poll is available.
    pollOptions = Pollmenu.objects.filter(hostel=hostel).count()
    if pollOptions > 0:
        return True
    else:
        return False

def checkVoted(uid):
    try:
        totalVotes = Pollvoting.objects.filter(uid = uid).count()
        if totalVotes > 0:
            return True
        else:
            return False
    except:
        return False
def pollPage(request):
    if not (isStudent(request)):
        return redirect('/crs/')
    # check if any poll is available for this student
    if not checkAvailabilityOfPoll(request.session.get('hostel')):
        return redirect('/crs/pollResult/')
        # redirect to page that shows that no poll is available!
    if checkVoted(request.session.get('uid')):
        return redirect('/crs/pollResult/')
    breakfastPollOptions = Pollmenu.objects.filter(hostel=request.session.get('hostel')).filter(type = 1)
    lunchPollOptions = Pollmenu.objects.filter(hostel=request.session.get('hostel')).filter(type = 2)
    dinnerPollOptions = Pollmenu.objects.filter(hostel=request.session.get('hostel')).filter(type = 3)
    sessionBreakfastArray = []
    sessionLunchArray = []
    sessionDinnerArray = []
    for x in breakfastPollOptions:
        sessionBreakfastArray.append(x.id)
    for x in lunchPollOptions:
        sessionLunchArray.append(x.id)
    for x in dinnerPollOptions:
        sessionDinnerArray.append(x.id)

    request.session['breakfastArray'] = sessionBreakfastArray
    request.session['lunchArray'] = sessionLunchArray
    request.session['dinnerArray'] = sessionDinnerArray

    return render_to_response("student/startPoll.html", {'list1' : breakfastPollOptions, 'list2' : lunchPollOptions, 'list3' : dinnerPollOptions})

def studentPolling(request):
    if not (isStudent(request)):
        return redirect('/crs/')
    # check if any poll is available for this student
    if not checkAvailabilityOfPoll(request.session.get('hostel')):
        return redirect('/crs/pollResult/')

    if checkVoted(request.session.get('uid')):
        return redirect('/crs/pollResult/')

    breakfastPOindex = request.POST.getlist('breakfast')
    lunchPOindex = request.POST.getlist('lunch')
    dinnerPOindex = request.POST.getlist('dinner')

    breakfastPollOptions = request.session.get('breakfastArray')
    lunchPollOptions = request.session.get('lunchArray')
    dinnerPollOptions = request.session.get('dinnerArray')

    voting = []

    for xx in breakfastPOindex:
        x = int(xx)
        if x > -1 and x < len(breakfastPollOptions):
            newObj = Pollvoting(id = breakfastPollOptions[x], uid = request.session.get('uid'))
            voting.append(newObj)
        else:
            return redirect('/crs/pollOptions/')
            # redirect page to polling page again
            # pass

    for xx in lunchPOindex:
        x = int(xx)
        if x > -1 and x < len(lunchPollOptions):
            newObj = Pollvoting(id = lunchPollOptions[x], uid = request.session.get('uid'))
            voting.append(newObj)
        else:
            return redirect('/crs/pollOptions/')
            # redirect page to polling page again
            pass

    for xx in dinnerPOindex:
        x = int(xx)
        if x > -1 and x < len(dinnerPollOptions):
            newObj = Pollvoting(id = dinnerPollOptions[x], uid = request.session.get('uid'))
            voting.append(newObj)
        else:
            return redirect('/crs/pollOptions/')
            # redirect page to polling page again
            pass
    for x in voting:
        x.save()

    return redirect('/crs/pollResult/')

class PollMenuVoting():
    """docstring for PollMenuVoting"""
    def __init__(self, arg, arg1):
        self.meal = arg.meal
        self.protein = arg.protein
        self.vitamin = arg.vitamin
        self.fat = arg.fat
        self.nutritions = arg.nutritions
        self.votes = arg1   
    def __str__(self):              # __unicode__ on Python 2
        return str(self.votes)

def pollResult(request):
    if not (isStudent(request) or isSecretary(request) or isWarden(request)):
        return redirect('/crs/')
    if not checkAvailabilityOfPoll(int(request.session.get('hostel'))):
        return finalPollResult(request)
    # breakfastPollOptions = request.session.get('breakfastArray')
    # lunchPollOptions = request.session.get('lunchArray')
    # dinnerPollOptions = request.session.get('dinnerArray')
    breakfastPollOptions = []
    lunchPollOptions = []
    dinnerPollOptions = []
    votesB = []
    votesL = []
    votesD = []
    dataB = ""
    dataL = ""
    dataD = ""
    b = 1
    l = 1
    d = 1
    try:
        breakfastPollOptions.extend(Pollmenu.objects.filter(hostel=request.session.get('hostel')).filter(type = 1))
    except:
        pass
    try:
        lunchPollOptions.extend(Pollmenu.objects.filter(hostel=request.session.get('hostel')).filter(type = 2))
    except:
        pass
    try:
        dinnerPollOptions.extend(Pollmenu.objects.filter(hostel=request.session.get('hostel')).filter(type = 3))
    except:
        pass
    for x in breakfastPollOptions:
        try:
            votesB.append(PollMenuVoting(x,Pollvoting.objects.filter(id=x.id).count()))
            dataB = dataB + "B-Item " + str(b) + "\t" + str(Pollvoting.objects.filter(id=x.id).count()) + "\n"
            b = b + 1
        except:
            votesB.append(PollMenuVoting(x,0))
            dataB = dataB + "B-Item " + str(b) + "\t0\n"
            b = b + 1
    for x in lunchPollOptions:
        try:
            votesL.append(PollMenuVoting(x,Pollvoting.objects.filter(id=x.id).count()))
            dataL = dataL + "L-Item " + str(l) + "\t" + str(Pollvoting.objects.filter(id=x.id).count()) + "\n"
            l = l + 1
        except:
            votesL.append(PollMenuVoting(x,0))
            dataL = dataL + "L-Item " + str(l) + "\t0\n"
            l = l + 1
    for x in dinnerPollOptions:
        try:
            votesD.append(PollMenuVoting(x,Pollvoting.objects.filter(id=x.id).count()))
            dataD = dataD + "D-Item " + str(d) + "\t" + str(Pollvoting.objects.filter(id=x.id).count()) + "\n"
            d = d + 1
        except:
            votesD.append(PollMenuVoting(x,0))
            dataD = dataD + "D-Item " + str(d) + "\t0\n"
            d = d + 1
    path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    print path
    with open(path+'/static/dataB.tsv', 'w') as f:
        myfile = File(f)
        myfile.write("meal\tvotes\n"+dataB)
    with open(path + '/static/dataL.tsv', 'w') as f:
        myfile = File(f)
        myfile.write("meal\tvotes\n"+dataL)
    with open(path + '/static/dataD.tsv', 'w') as f:
        myfile = File(f)
        myfile.write("meal\tvotes\n"+dataD)
    return render_to_response("student/pollResult.html", {'list1' : votesB, 'list2' : votesL, 'list3' : votesD , 'msg': request.session.get('name')})

def OpenHostelPage(request):
    if not (isStudent(request) or isSecretary(request)):
        return redirect("/crs/")
    obj=Student.objects.get(uid=request.session.get('uid'))
    print str(obj.hostel)
    if isStudent(request):
        return render_to_response('student/studHostelLeave.html',{'list' : obj, 'msg': request.session.get('name')}, context_instance=RequestContext(request))
    else:
        return render_to_response('secretary/studHostelLeave.html',{'list' : obj, 'msg': request.session.get('name')}, context_instance=RequestContext(request))

##GetDifferece(start_date,end_date)
#Function takes 2 dates as arguments and @return Boolean True is start_date < end_sate
def getDiffrence(start_date,end_date):
    sYear = int(start_date[0:4])
    eYear = int(end_date[0:4])
    sMonth = int(start_date[5:7])
    eMonth = int(end_date[5:7])
    sDay = int(start_date[8:10])
    eDay = int(end_date[8:10])
    start_time= 0
    end_time = 0
    try:
        start_time = int(datetime.datetime(sYear,sMonth,sDay).strftime('%s'))
        end_time = int(datetime.datetime(eYear,eMonth,eDay).strftime('%s'))
    except:
        return False

    if end_time - start_time <= 0:
        return False
    else:
        if start_time - int(datetime.datetime.now().strftime('%s')) <= 86400:
            return False
        else:
            return True

def HostelLeavingSubmit(request):
    # laptop=request.POST.get('laptop', '')
    if not (isStudent(request) or isSecretary(request)):
        return redirect("/crs/")
    start_date=request.POST.get('start_date', '')
    end_date=request.POST.get('end_date' , '')
    destination=request.POST.get('destination', '')
    reason=request.POST.get('reason', '')
    time = request.POST.get('time','')
    username=request.session.get("username")
    print start_date;
    # obj = Student.objects.get(username=username)
    match = re.match(r'^20[0-9][0-9]-[0-1][0-9]-[0-3][0-9]$', start_date)
    if match:
        pass
    else:
        return HttpResponse("start date is invalid")
    match = re.match(r'^20[0-9][0-9]-[0-1][0-9]-[0-3][0-9]$', start_date)
    if match:
        pass
    else:
        return HttpResponse("end date is invalid")
    print time
    match = re.match(r'^[0-2][0-9]:[0-5][0-9]$', time)
    print match
    if match:
        hours = int(time[0:2])
        if hours > 23 :
            return HttpResponse('Invalid time! Hour > 23')
    else:
        return HttpResponse('Invalid time!')
    destination = validateText(destination)
    reason = validateText(reason)
    if len(destination) == 0 or len(destination) == 0:
        return HttpResponse("reason or destination invalid!")
    # rollno = obj.roll
    hostel = request.session.get('hostel')
    # roll = obj.roll
    mobile=request.POST.get('mobile') 
    match = re.match(r'^\d\d\d\d\d\d\d\d\d\d$', mobile)
    if match:
        pass
    else:
        return HttpResponse("invalid mobile number!")
    #Now validate the time difference
    if not getDiffrence(start_date,end_date):
        return HttpResponse("Error in Date input")

    hostel = HostelLeavingInformation(studid = request.session.get('uid'), start_date = start_date, end_date = end_date, destination = destination,reason = reason , time = time, hostel = hostel, mobile = mobile, status = 0)
    hostel.save()
    #redirect to page where all hostel leaving forms can be viewed!
    return redirect('/viewPastForm/');

def viewPastHostelLeaveForms(request):
    if (isStudent(request) or isSecretary(request)):
        forms = []
        try:
            forms.extend(HostelLeavingInformation.objects.filter(studid = request.session.get('uid')))
        except:
            pass
        if isStudent(request):
            return render_to_response('student/previousleave.html', {'list' : forms, 'msg': request.session.get('name')})
        else:
            return render_to_response('secretary/previousleave.html', {'list' : forms, 'msg': request.session.get('name')})
    elif isWarden(request):
        forms = []
        try:
            forms.extend(HostelLeavingInformation.objects.filter(hostel = request.session.get('hostel')))
        except:
            pass
        return render_to_response('warden/newLeaveApplication.html', {'list' : forms, 'msg': request.session.get('name')})

def viewForm(request,formID):
    if isStudent(request) or isSecretary(request):
        form = None
        try:
            form = HostelLeavingInformation.objects.get(studid=request.session.get('uid'), sno = int(formID) )
        except:
            return HttpResponse('Not authorized to view this page!')

        student = Student.objects.get(uid=request.session.get('uid'))
        if isStudent(request):
            return render_to_response('student/applicationDetail.html', {'item' : form, 'student' : student, 'warden' : False})
        else:
            return render_to_response('secretary/applicationDetail.html', {'item' : form, 'student' : student, 'warden' : False})
    elif isWarden(request):
        form = None
        print request.session.get('hostel')
        print formID
        try:
            form = HostelLeavingInformation.objects.get(sno = int(formID), hostel = request.session.get('hostel'))
        except:
            return HttpResponse('Not authorized to view this page!')

        student = Student.objects.get(uid=form.studid)
        return render_to_response('warden/applicationDetail.html', {'item' : form, 'student' : student, 'warden' : True})
    else:
        redirect('/crs/')

def approveForm(request,formID):
    if isWarden(request):
        print "Form id = " + formID + " hostel" + request.Session.get('hostel')
        try:
            form = HostelLeavingInformation.objects.get(sno = int(formID), hostel = request.session.get('hostel'))
            form.status = 1
            form.save()
        except:
            return HttpResponse('Not authorized to view this page!')
    return redirect('/viewPastForm/')

def rejectForm(request,formID):
    if isWarden(request):
        print "Form id = " + formID + " hostel " + str(request.session.get('hostel'))
        try:
            form = HostelLeavingInformation.objects.get(sno = int(formID), hostel = request.session.get('hostel'))
            form.status = 2
            form.save()
        except:
            return HttpResponse('Not authorized to view this page!')
    # else:
    #     return redirect('/viewPastForm/')    
    return redirect('/viewPastForm/')

def downloadPDF(request, formID):
    form = None
    stud = None
    if isStudent(request) or isSecretary(request):
        try:
            form = HostelLeavingInformation.objects.get(studid=request.session.get('uid'), sno = int(formID) )
        except:
            return HttpResponse('Not authorized to view this page!')

        stud = Student.objects.get(uid=request.session.get('uid'))
    elif isWarden(request):
        form = None
        print request.session.get('hostel')
        print formID
        try:
            form = HostelLeavingInformation.objects.get(sno = int(formID), hostel = request.session.get('hostel'))
        except:
            return HttpResponse('Not authorized to view this page!')

        stud = Student.objects.get(uid=form.studid)
    else:
        return HttpResponse("Not authorized to view this page!")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="experiment.pdf";pagesize=landscape(letter)'
    p = canvas.Canvas(response)
    name = stud.name
    print name
    room = str(stud.room)
    print room
    start_date = (str(form.start_date))[0:19]
    print start_date
    end_date = (str(form.end_date))[0:19]
    print end_date
    time = (str(form.time))[0:19]
    print time
    hostel = Hostel.objects.get(id = stud.hostel).name
    print hostel
    destination = form.destination
    if len(destination) > 30:
        destination = destination[0:30] + "..."
    print destination
    print str(len(destination))
    reason = form.reason
    if len(reason) > 20:
        reason = reason[0:20] + "..."
    print reason
    print str(len(reason))
    rollno = stud.roll
    print rollno
    mobile = form.mobile
    print mobile
    formid = str(form.sno)
    print formid
    currentTime = str(datetime.datetime.now())[0:19]
    print currentTime
    status = int(form.status)
    # print status
    if (status == 0):
        status = "Approval Pending"
    elif status == 1:
        status = "Approved"
    else:
        status = "Rejected"
    curTime = (datetime.datetime.now() + timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d %H:%M:%S')
    path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    image = path + "/Hostel_Leaving_Form.png"
    p.drawImage(image,20,40,width=600,height=800)
    p.setFont('Helvetica', 15, leading=None)
    p.drawString(140, 670, name)
    p.drawString(400, 645, room)
    p.drawString(145, 620, hostel)
    p.setFont('Helvetica', 10, leading=None)
    p.drawString(205, 595, start_date)
    p.drawString(286, 595, end_date)
    p.setFont('Helvetica', 15, leading=None)
    p.drawString(380, 595, time)
    p.drawString(286, 572, destination)
    p.drawString(140, 545, reason)
    # p.drawString(286, 595, end_date)
    p.drawString(194, 458, rollno)
    p.drawString(306, 441, mobile)
    p.drawString(130, 375, hostel)
    p.drawString(186, 304, formid)
    p.drawString(180, 287, status)
    p.drawString(180, 270, curTime)
    p.drawString(135, 205, name)
    p.drawString(380, 205, rollno)
    p.drawString(157, 171, hostel)
    p.drawString(350, 171, room)
    p.setFont('Helvetica', 10, leading=None)
    p.drawString(115, 139, start_date)
    p.drawString(200, 139, end_date)
    p.showPage()
    p.save()
    return response
