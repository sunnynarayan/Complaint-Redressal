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
from student.views import getTypeDescription,getCatagory


def wardenComplainView(request):

	uid=request.session.get('uid')		
	# PublicComplainObjects = Complainlink.objects.all().filter(wardenid = uid).filter(studid = 0);
	query1 = 'SELECT * FROM complainLink WHERE wardenID = ' + str(uid) + ' AND studID = 0'
	PublicComplainObjects = Complainlink.objects.raw(query1)
	query2 = 'SELECT * FROM complainLink WHERE wardenID = ' + str(uid) + ' AND studID != 0'
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
	return render_to_response('warden/wardenViewComplain.html',{'list1' : Publiclist, 'list2':Privatelist});


def wardenHome(request):
	try:
		uid=request.session.get('uid')
		return render_to_response('warden/wardenHome.html');
	except:
		return render_to_response('login/loginPage.html');

def wardenProfile(request):
	try:
		uid=request.session.get('uid')
		return render_to_response('warden/wardenProfile.html');
	except:
		return render_to_response(login/loginPage.html);

def viewSecretary(request):
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
	try:
		uid=request.session.get('uid');
		obj=Faculty.objects.get(fid=uid);
		mobile=request.POST['mobile'];
		obj.mobile=mobile;
		obj.save();
	except:
		return render_to_response('login/loginPage.html');

