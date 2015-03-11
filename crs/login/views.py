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

def logout(request):
	request.session['login']="False";
	request.session.flush()
	return redirect('/crs/')
def validatePassword(passwd):
	return ((len(passwd) > 20) or (len(passwd) < 8))

def login(request):
	try:
		if request.session.get("login") == "True":							#check if the user is already logged in
			if request.session.get("user_type")=="faculty" :		#if yes then redirect the request to home page according to whether faculty or student
				return render_to_response('warden/wardenViewComplain.html');
			elif request.session.get("user_type")=="secretary" :
				return render_to_response('secretary/secHome.html');
			else:
				return render_to_response('student/studentBase.html');

	except NameError:
		return render_to_response('login/loginPage.html', {'msg':''});	

	return render_to_response('login/loginPage.html', {'msg':''});		#if not then display the login page

def afterLogin(request):								#after login function working
	uname = request.POST.get('username','');
	passwd = request.POST.get('password','');
	if re.sub('[a-z.@0-9]',"",uname) != "":				#check username for possible SQL injection and other injections
		return render_to_response('login/loginPage.html', {'msg':'Errornous user'}); #Error in username entry !!, append error message
	if validatePassword(passwd):
		return render_to_response('login/loginPage.html', {'msg':'error in password'}); #Error in password, append error message

	hash_object = hashlib.sha256(b""+passwd)
	passwd = hash_object.hexdigest()
	# passwd = make_password(passwd);		#Hashing/encrypting the password for further use
	if uname.endswith("fac"):
		try:
			uname = uname.replace("@fac","")
			obj=Faculty.objects.get(username=uname,password=passwd);		#username  in fac table
			request.session['login']="True";
			request.session['username']=uname;
			request.session['user_type']="faculty";
			request.session['uid']= obj.fid;
			if uname=='nalin':
				return render_to_response('wardenOffice/wardenHome.html', {'msg' : obj.name});
			else:
				return render_to_response('warden/wardenBase.html', {'msg' : obj.name})
		except:
			return render_to_response('login/loginPage.html', {'msg':'invalid user: '+uname + 'password : ' + passwd});
	elif uname.endswith("stud"):
		try:
			uname = uname.replace("@stud","")
			obj = Student.objects.get(username=uname,password=passwd);	#username  in stud table
			request.session['login']="True";
			request.session['username'] = uname;
			request.session['name'] = obj.name;
			request.session['hostel']= obj.hostel;
			request.session['uid'] = obj.uid;

			if obj.issec==1:                    
				request.session['user_type']="secretary";
				return render_to_response('secretary/secHome.html', {'msg':obj.name}); 
			else:
				request.session['user_type']="student";
				return render_to_response('student/studentBase.html', {'msg':obj.name});

		except:
			return render_to_response('login/loginPage.html', {'msg' : 'unknown user(line74) : ' + uname + "pass : " + passwd});
	else:
		return render_to_response('login/loginPage.html', {'msg' : 'username recieved(line76) : ' + uname + "pass : " + passwd});

def changePasswd(request):
	return render_to_response('login/resetPasswd.html', {'Err' : ''})

def resetPasswd(request):
	uid = request.session.get("uid")
	oldPasswd = request.POST.get('oldPasswd','')
	newPasswd = request.POST.get('newPasswd1','')
	newPasswd2 = request.POST.get('newPasswd2','')

	if validatePassword(oldPasswd) or validatePassword(newPasswd) or validatePassword(newPasswd2):
		return render_to_response('login/resetPasswd.html', {'Err':'Password length must be between 8 & 20'})

	hash_object = hashlib.sha256(b""+oldPasswd)
	oldPasswd = hash_object.hexdigest()

	hash_object = hashlib.sha256(b""+newPasswd)
	newPasswd = hash_object.hexdigest()

	hash_object = hashlib.sha256(b""+newPasswd2)
	newPasswd2 = hash_object.hexdigest()

	if newPasswd != newPasswd2 :
		return render_to_response('login/resetPasswd.html', {'Err' : 'Password mismatch in New Password'})
	
	if(request.session.get("user_type") == 	"student" or request.session.get("user_type") == "secretary"):
		try:
			obj = Student.objects.get(uid=uid,password=oldPasswd)
			obj.password = newPasswd
			obj.save()
		except:
			return render_to_response('login/resetPasswd.html', {'Err' : 'old Password is Wrong!'})
	else:
		try:
			obj = Faculty.objects.get(uid=uid,password=oldPasswd)
			obj.password = newPasswd
			obj.save()
		except:
			return render_to_response('login/resetPasswd.html', {'Err' : 'old Password is Wrong!'})
	return render_to_response('login/resetPasswd.html', {'Err' : 'Password changed successfully'})
