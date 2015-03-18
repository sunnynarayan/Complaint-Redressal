from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.context_processors import csrf
from django.contrib.sessions.models import Session
import hashlib
import datetime
from login.models import *
import re
from django.db import connection

def isSecretary(request):
	user_type = request.session.get("user_type",'')
	if user_type != "secretary":
		return False
	else:
		return True

def secComplainView(request):
	if not (isSecretary(request)):
		return redirect('/crs/')
	uid=request.session.get('uid')
	pubComplains = Complain.objects.raw('SELECT * FROM `complain`, complainLink WHERE (complain.status = 1 OR complain.status=2 OR complain.status=3 OR complain.status=11 OR complain.status=12 OR complain.status=13) AND (complainLink.secID = ' + str(uid) + ' AND complainLink.studID = 0) AND complain.cid = complainLink.CID')
	priComplains = Complain.objects.raw('SELECT * FROM `complain`, complainLink WHERE (complain.status = 1 OR complain.status=2 OR complain.status=3 OR complain.status=11 OR complain.status=12 OR complain.status=13) AND (complainLink.secID = ' + str(uid) + ' AND complainLink.studID != 0) AND complain.cid = complainLink.CID')
	return render_to_response('secretary/listComp.html',{'public' : pubComplains, 'private' : priComplains});

def secLodgeComplain(request):
	if not (isSecretary(request)):
		return redirect('/crs/')
	return render_to_response('secretary/secComp.html');

def forwardToWarden(request):
	if not (isSecretary(request)):
		return redirect('/crs/')
	complainArray=request.POST.getlist('complain')
	length = len(complainArray)
	for x in range(0,length):
		comid = complainArray[x]
		ClO =Complainlink.objects.get(cid=comid)
		ClO.woid = "1235"
		ClO.save()
		obj=Complain.objects.get(cid=ClO.cid)
		if obj.status==1:
			obj.status==2
			obj.save()
		else:
			obj.save()
	# complainObj.wardenID = wardenID
	# complainObj.save()
	return redirect('../listComp/',{'msg':'Succesfully Redirected!!!'})

def rejectComplain(request):
	if not (isSecretary(request)):
		return redirect('/crs/')
	complainArray=request.POST.getlist('complain')
	length = len(complainArray)
	for x in range(0,length):
		comid = complainArray[x]
		obj=Complain.objects.get(cid=ClO.cid)
		obj.status=21
		obj.save()
	# complainObj.wardenID = wardenID
	# complainObj.save()
	return redirect('../listComp/',{'msg':'Succesfully Redirected!!!'})

def secViewComplain(request):
    indexF = request.GET.get('CID')
    index = int(indexF)
    qry = "SELECT * FROM complain a, complainLink b WHERE b.CID = " + str(index) + " AND (b.secID = " + str(request.session.get('uid')) + " OR b.studID = 0 ) AND b.CID = a.cid"
    complainObject = Complain.objects.raw(qry)
    return render_to_response("secretary/compDetail.html", {'item': complainObject[0]})

 #    if not (isSecretary(request)):
	# 	return redirect('/crs/')
	# uid=request.session.get('uid')
	# pubComplains = Complain.objects.raw('SELECT * FROM `complain`, complainLink WHERE (complainLink.secID = uid OR complainLink.studID = 0) AND complain.cid = complainLink.CID')
	# priComplains = Complain.objects.raw('SELECT * FROM `complain`, complainLink WHERE (complainLink.studID = uid) AND complain.cid = complainLink.CID')
	# return render_to_response('secretary/listComp.html',{'public' : pubComplains, 'private' : priComplains});


# def editProfile(request):
# 	return redirect('//')


# def lodgeComplainDetail(request):
# 	subject=request.POST.get('subject');
# 	detail=request.POST.get('message');
# 	catagory=getCatagory(request.POST.get('catagory'));
# 	hostel=request.session.get("hostel");
# 	time=datetime.datetime.now();
# 	public = (request.POST.get('complainType') == "0");
# 	uid=request.session.get('uid');	
# 	history = "Complain added by " + request.session.get("name") + " at time : " + str(time) 
# 	complainObj=Complain(uid = uid , time = time , hostel = hostel, type=catagory , subject	= subject, detail = detail, comments = 0, history = history );
# 	complainObj.save();
# 	secretaryObj = Secretary.objects.get(hostel=hostel, type=catagory)
# 	secid = secretaryObj.uid
# 	cid=(Complain.objects.get(uid = uid , time = time)).cid
# 	if (public == True):
# 		CLObj = Complainlink(cid = cid, studid = 0, secid = secid)
# 		CLObj.save()
# 	else:		
# 		CLObj = Complainlink(cid = cid, studid = uid, secid = secid)
# 		CLObj.save()
# 	return redirect('../listComp/');
	
# def studentComplainView(request):
# 	# isStudent(request)
# 	uid=request.session.get('uid')
# 	ComplainObjects = Complain.objects.raw('SELECT * FROM `complain`, complainLink WHERE (complainLink.studID = ' + str(uid) + ' OR complainLink.studID = 0) AND complain.cid = complainLink.CID')
# 	return render_to_response('student/viewStudComplain.html',{'list' : ComplainObjects});

# ComplainObjects = Complain.objects.raw('SELECT * FROM `complain`, complainLink, WHERE (complainLink.studID = 1000 OR complainLink.studID = 0) AND complain.cid = complainLink.CID')


# def studentComplainView(request):
# 	uid=request.session.get('uid')
# 	ComplainObjects = Complain.objects.all().filter(uid = uid)
# 	return render_to_response('student/viewStudComplain.html',{'list' : ComplainObjects});

	
# def studentLodgeComplain(request):
# 	return render_to_response('student/studLodgeComplain.html');

# def studentHome(request):
# 	return render_to_response('student/studentHome.html');

# def studentProfile(request):
# 	return render_to_response('student/studentProfile.html');

# def studentViewRate(request):
# 	return render_to_response('student/studViewRate.html');

# def studentPoll(request):
# 	return render_to_response('student/studPoll.html');

# def studentHostelLeave(request):
# 	return render_to_response('student/studHostelLeave.html');

# def studentMessRebate(request):
# 	return render_to_response('student/messrebate.html');

# def getCatagory(str):
# 	if str == "Mess":
# 		return 1
# 	elif str == "Environment":
# 		return 2
# 	elif str == "Technical":
# 		return 3
# 	elif str == "Maintenance":
# 		return 4
# 	else:
# 		return 0

# def getTypeDescription(code):
# 	if code == 1:
# 		return "Mess"
# 	elif code == 2:
# 		return "Environment"
# 	elif code == 3:
# 		return "Technical"
# 	elif code == 4:
# 		return "Maintenance"
# 	else:
# 		return "Other"
