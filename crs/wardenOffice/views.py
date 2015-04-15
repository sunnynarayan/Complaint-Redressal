from django.shortcuts import render
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.sessions.models import Session
import hashlib
import datetime
from login.models import *
import re
from student.views import *

def isWardenOffice(request):
	user_type = request.session.get("user_type",'')
	if user_type != "wardenOffice":
		return False
	else:
		return True

def wardenOfficeComplainView(request):
	if not (isWardenOffice(request)):
		return redirect('/crs/')
	uid=request.session.get('uid')
	# PublicComplainObjects = Complainlink.objects.all?().filter(wardenid = uid).filter(studid = 0);
	# query1 = 'SELECT * FROM complainLink WHERE woID = ' + str(uid) + ' AND studID = 0'
	# query2 = 'SELECT * FROM complainLink WHERE woID = ' + str(uid) + ' AND studID != 0'
	query1 = 'SELECT * FROM `complain`, complainLink WHERE (complain.status = 2 OR complain.status = 22 OR complain.status=12 OR complain.status=3 OR complain.status=23 OR complain.status=13) AND (complainLink.woID = ' + str(uid) + ' AND complainLink.studID = 0) AND complain.cid = complainLink.CID'
	query2 = 'SELECT * FROM `complain`, complainLink WHERE (complain.status = 2 OR complain.status=22 OR complain.status=12 OR complain.status=3 OR complain.status=23 OR complain.status=13) AND (complainLink.woID = ' + str(uid) + ' AND complainLink.studID != 0) AND complain.cid = complainLink.CID'
	PublicComplainObjects = Complainlink.objects.raw(query1)
	PrivateComplainObjects = Complainlink.objects.raw(query2)
	# PrivateComplainObjects=Complainlink.objects.all().filter(wardenid = uid).exclude(studid = 0);
	Privatelist=[];
	Publiclist=[];
	for num in PrivateComplainObjects:
		numCid=num.cid
		Privatelist.append(Complain.objects.get(cid=numCid));		#username  in fac table
	for num in PublicComplainObjects:
		numCid=num.cid
		Publiclist.append(Complain.objects.get(cid=numCid));
	return render_to_response('wardenOffice/wardenHome.html',{'list1' : Publiclist, 'list2':Privatelist, 'msg': request.session.get('name')});

def wardenOfficeViewComplain(complainObject):
    # indexF = request.GET.get('CID')
    # index = int(indexF)
    # qry = "SELECT * FROM complain a, complainLink b WHERE b.CID = " + str(index) + " AND (b.secID = " + str(request.session.get('uid')) + " OR b.studID = 0 ) AND b.CID = a.cid"
    # complainObject = Complain.objects.raw(qry)
    # return render_to_response("secretary/complainDetail.html", {'item': complainObject[0]})
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
    return render_to_response("secretary/complainDetail.html", {'item': complainObject[0],'documents':documents,'comment':comment})
def wardenOfficeHome(request):
	if not (isWardenOffice(request)):
		return redirect('/crs/')
	return render_to_response('wardenOffice/wardenHome.html', {'msg' : request.session.get('name') });

def forwardToWarden(request):
	if not (isWardenOffice(request)):
		return redirect('/crs/')
	complainArray=request.POST.getlist('complain')
	length = len(complainArray)
	for x in range(0,length):
		comid = complainArray[x]
		ClO =Complainlink.objects.get(cid=comid)
		hostel=(Complain.objects.get(cid=comid)).hostel
		wardenId = (Warden.objects.get(hostel=hostel)).fid
		ClO.wardenid = wardenId
		obj=Complain.objects.get(cid=ClO.cid)
		ClO.save()
		if obj.status==2:
			obj.status=3
			obj.save()
		elif obj.status==12:
			obj.status=13
			obj.save()
		else:
			obj.status=23
			obj.save()	
	# complainObj.wardenID = wardenID
	# complainObj.save()
	return redirect('../wardenComplain');

def getHostelType(hostelstr):
	if hostelstr == "Ashoka":
		return 1
	elif hostelstr == "Aryabhatta":
		return 2
	elif hostelstr == "Chanakya1":
		return 3
	elif hostelstr == "Chanakya2":
		return 4
	elif hostelstr == "GBH":
		return 5
	else:
		return 0

def isAddressed(address):
	if address == "Addressed":
		return 0
	elif address == "New":
		return 1
	else:
		return 2

def complainType(typec):
	if typec=="Mess":
		return 1
	elif typec=="Environment":
		return 2
	elif typec=="Technical":
		return 3
	elif typec=="Maintenance":
		return 4
	elif typec=="Mess":
		return 5
	else:
		return 6


def showHostelWiseComplain(request,hostel,isadd):
	if not (isWardenOffice(request)):
		return redirect('/crs/')
	uid=request.session.get('uid')
	hostelType = getHostelType(hostel)
	isadd=isAddressed(isadd)
	if hostelType == 0:
		return HttpResponse('error')
	if isadd==1:
		query1 = 'SELECT * FROM `complain`, complainLink WHERE (complain.status = 2 OR complain.status = 22 OR complain.status=12 OR complain.status=3 OR complain.status=23 OR complain.status=13) AND (complainLink.woID = ' + str(uid) + ' AND complainLink.studID = 0) AND complain.cid = complainLink.CID AND complain.hostel = ' + str(hostelType)
		query2 = 'SELECT * FROM `complain`, complainLink WHERE (complain.status = 2 OR complain.status=22 OR complain.status=12 OR complain.status=3 OR complain.status=23 OR complain.status=13) AND (complainLink.woID = ' + str(uid) + ' AND complainLink.studID != 0) AND complain.cid = complainLink.CID AND complain.hostel = ' + str(hostelType)
	elif isadd==0:
		query1 = 'SELECT * FROM `complain`, complainLink WHERE complain.status=0 AND (complainLink.woID = ' + str(uid) + ' AND complainLink.studID = 0) AND complain.cid = complainLink.CID AND complain.hostel = ' + str(hostelType)
		query2 = 'SELECT * FROM `complain`, complainLink WHERE complain.status=0 AND (complainLink.woID = ' + str(uid) + ' AND complainLink.studID != 0) AND complain.cid = complainLink.CID AND complain.hostel = ' + str(hostelType)	
	else:
		return HttpResponse('error')	
	PublicComplainObjects = Complainlink.objects.raw(query1)
	PrivateComplainObjects = Complainlink.objects.raw(query2)
	# PrivateComplainObjects=Complainlink.objects.all().filter(wardenid = uid).exclude(studid = 0);
	Privatelist=[];
	Publiclist=[];
	for num in PrivateComplainObjects:
		numCid=num.cid
		Privatelist.append(Complain.objects.get(cid=numCid));		#username  in fac table
	for num in PublicComplainObjects:
		numCid=num.cid
		Publiclist.append(Complain.objects.get(cid=numCid));
	return render_to_response('wardenOffice/wardenHome.html',{'list1' : Publiclist, 'list2':Privatelist, 'msg': request.session.get('name')});

def showHostelTypeWiseComplain(request,hostel,typeComplain):
	if not (isWardenOffice(request)):
		return redirect('/crs/')
	uid=request.session.get('uid')
	hostelType = getHostelType(hostel)
	typec = complainType(typeComplain)
	if hostelType == 0 or typec==6:
		return HttpResponse('error')
	query1 = "SELECT * FROM complain, complainLink WHERE (complain.status = 2 OR complain.status = 22 OR complain.status=12 OR complain.status=3 OR complain.status=23 OR complain.status=13) AND (complainLink.woID = " + str(uid) + " AND complainLink.studID = 0) AND complain.cid = complainLink.CID AND complain.hostel = " + str(hostelType) + " AND complain.type = " + str(typec)
	query2 = 'SELECT * FROM complain, complainLink WHERE (complain.status = 2 OR complain.status=22 OR complain.status=12 OR complain.status=3 OR complain.status=23 OR complain.status=13) AND (complainLink.woID = ' + str(uid) + ' AND complainLink.studID != 0) AND complain.cid = complainLink.CID AND complain.hostel = ' + str(hostelType) + ' AND complain.type = ' +  str(typec)
	PublicComplainObjects = Complainlink.objects.raw(query1)
	PrivateComplainObjects = Complainlink.objects.raw(query2)
	PrivateComplainObjects=Complainlink.objects.all().filter(wardenid = uid).exclude(studid = 0);
	Privatelist=[];
	Publiclist=[];
	for num in PrivateComplainObjects:
		numCid=num.cid
		Privatelist.append(Complain.objects.get(cid=numCid));		#username  in fac table
	for num in PublicComplainObjects:
		numCid=num.cid
		Publiclist.append(Complain.objects.get(cid=numCid));
	return render_to_response('wardenOffice/wardenHome.html',{'list1' : Publiclist, 'list2':Privatelist, 'msg': request.session.get('name')});

def showHostelAdUnadWiseComplain(request,hostel,typec,isadd):
	if not (isWardenOffice(request)):
		return redirect('/crs/')
	uid=request.session.get('uid')
	hostelType = getHostelType(hostel)
	typec=complainType(typec)
	addressed=isAddressed(isadd)
	if hostelType==0   or typec == 6 or addressed == 2:
		return HttpResponse('error1')
	if addressed==1:
		query1 = 'SELECT * FROM complain, complainLink WHERE (complain.status = 2 OR complain.status = 22 OR complain.status=12 OR complain.status=3 OR complain.status=23 OR complain.status=13) AND (complainLink.woID = ' + str(uid) + ' AND complainLink.studID = 0) AND complain.cid = complainLink.CID AND complain.hostel = ' + str(hostelType) + ' AND complain.type = ' + str(typec)
		query2 = 'SELECT * FROM `complain`, complainLink WHERE (complain.status = 2 OR complain.status=22 OR complain.status=12 OR complain.status=3 OR complain.status=23 OR complain.status=13) AND (complainLink.woID = ' + str(uid) + ' AND complainLink.studID != 0) AND complain.cid = complainLink.CID AND complain.hostel = ' + str(hostelType) + ' AND complain.type = ' + str(typec)
	elif addressed==0:
		query1 = 'SELECT * FROM `complain`, complainLink WHERE complain.status=0 AND (complainLink.woID = ' + str(uid) + ' AND complainLink.studID = 0) AND complain.cid = complainLink.CID AND complain.hostel = ' + str(hostelType) + ' AND complain.type = ' + str(typec)
		query2 = 'SELECT * FROM `complain`, complainLink WHERE complain.status=0 AND (complainLink.woID = ' + str(uid) + ' AND complainLink.studID != 0) AND complain.cid = complainLink.CID AND complain.hostel = ' + str(hostelType) + ' AND complain.type = ' + str(typec)
	else:
		return HttpResponse('error2')
	PublicComplainObjects = Complainlink.objects.raw(query1)
	PrivateComplainObjects = Complainlink.objects.raw(query2)
	# PrivateComplainObjects=Complainlink.objects.all().filter(wardenid = uid).exclude(studid = 0);
	Privatelist=[];
	Publiclist=[];
	for num in PrivateComplainObjects:
		numCid=num.cid
		Privatelist.append(Complain.objects.get(cid=numCid));		#username  in fac table
	for num in PublicComplainObjects:
		numCid=num.cid
		Publiclist.append(Complain.objects.get(cid=numCid));
	return render_to_response('wardenOffice/wardenHome.html',{'list1' : Publiclist, 'list2':Privatelist, 'msg': request.session.get('name')});


def showHostelSecWiseInfo(request,hostel):
	if not (isWardenOffice(request)):
		return redirect('/crs/')
	uid=request.session.get('uid')
	hostelType = getHostelType(hostel)
	if hostelType == 0:
		return HttpResponse('error')
	obj1=Secretary.objects.filter(hostel=hostelType)
	stud=[]
	for sec in obj1:
		stud.append(Student.objects.get(uid=sec.uid))
	# obj=Student.objects.filter()
	# return HttpResponse(obj)
	return render_to_response('wardenOffice/viewSecretary.html',{'list1':obj1,'list2':stud})


def showHostelStudWiseInfo(request,hostel):
	if not (isWardenOffice(request)):
		return redirect('/crs/')
	uid=request.session.get('uid')
	hostelType = getHostelType(hostel)
	if hostelType == 0:
		return HttpResponse('error')
	obj=Student.objects.filter(hostel=hostelType)
	# return HttpResponse(obj)
	return render_to_response('wardenOffice/viewStudent.html',{'list':obj})


def viewSecretary(request):
	if not (isWardenOffice(request)):
		return redirect('/crs/')
	# try:
	uid=request.session.get('uid')
	ashokaseclist=[];
	aryabhattaseclist=[];
	chanakya1seclist=[];
	chanakya2seclist=[];
	test=[1,2,3,4];
	for num in test:
		ashokaseclist.append(Secretary.objects.filter(hostel = 0).filter(type = num));
		aryabhattaseclist.append(Secretary.objects.filter(hostel = 1).filter(type = num));
		chanakya1seclist.append(Secretary.objects.filter(hostel = 2).filter(type = num));
		chanakya2seclist.append(Secretary.objects.filter(hostel = 3).filter(type = num));
	return render_to_response('wardenOffice/wardenOfficeViewComplain.html',{'list1':ashokaseclist, 'list2' :aryabhattaseclist,'list3':chanakya1seclist,'list4':chanakya2seclist});
	# except:
	# 	return render_to_response('login/loginPage.html');

# def ForwardComplain(request):
	# try:
		# uid=request.session.get('uid');
		# 
	# except:
		# return render_to_response('login/loginPage.html');



# Create your views here.

