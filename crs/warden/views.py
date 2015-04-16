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
from Scheduling import *

def isWarden(request):
	user_type = request.session.get("user_type",'')
	if user_type != "warden":
		return False
	else:
		return True


def wardenComplainView(request):
	if not (isWarden(request)):
		return redirect('/crs/')
	uid=request.session.get('uid')		
	# PublicComplainObjects = Complainlink.objects.all().filter(wardenid = uid).filter(studid = 0);
	# query1 = 'SELECT * FROM complainLink WHERE wardenID = ' + str(uid) + ' AND studID = 0'
	query1 = 'SELECT * FROM `complain`, complainLink WHERE (complain.status = 3 OR complain.status = 13 OR complain.status = 23) AND (complainLink.wardenid = ' + str(uid) + ' AND complainLink.studID = 0) AND complain.cid = complainLink.CID'
	query2 = 'SELECT * FROM `complain`, complainLink WHERE (complain.status = 3 OR complain.status =  13 OR complain.status = 23) AND (complainLink.wardenid = ' + str(uid) + ' AND complainLink.studID != 0) AND complain.cid = complainLink.CID'
	PublicComplainObjects = Complainlink.objects.raw(query1)
	# query2 = 'SELECT * FROM complainLink WHERE wardenID = ' + str(uid) + ' AND studID != 0'
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
	return render_to_response('warden/wardenViewComplain.html',{'list1' : Publiclist, 'list2': Privatelist})
	##
	# return Schedule(request)

def wardenViewComplain(complainObject):
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

def wardenHome(request):
	if not (isWarden(request)):
		return redirect('/crs/')
	try:
		uid=request.session.get('uid')
		return render_to_response('warden/wardenHome.html');
	except:
		return render_to_response('login/loginPage.html');

def wardenProfile(request):
	if not (isWarden(request)):
		return redirect('/crs/')

	try:
		uid=request.session.get('uid')
		return render_to_response('warden/wardenProfile.html');
	except:
		return render_to_response(login/loginPage.html);

def viewSecretary(request):
	if not (isWarden(request)):
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
	return render_to_response('warden/wardenViewComplain.html',{'list1':ashokaseclist, 'list2' :aryabhattaseclist,'list3':chanakya1seclist,'list4':chanakya2seclist});
	# except:
	# 	return render_to_response('login/loginPage.html');

def wardenEditProfile(request):
	if not (isWarden(request)):
		return redirect('/crs/')
		
	try:
		uid=request.session.get('uid');
		obj=Faculty.objects.get(fid=uid);
		mobile=request.POST['mobile'];
		obj.mobile=mobile;
		obj.save();
	except:
		return render_to_response('login/loginPage.html');

