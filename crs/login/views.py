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
from datetime import timedelta
from login.models import *
from warden.views import isWarden
from secretary.views import *
from student.views import *
from wardenOffice.views import *
import re
from django.core.mail import send_mail
from django.core.context_processors import csrf
from django.views.decorators.csrf import requires_csrf_token
from random import randint
##This function clears the whole session array and explicitely sets request.session['logout'] to "False". All users use this
#function

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

def isWardenOffice(request):
	user_type = request.session.get("user_type",'')
	if user_type != "wardenOffice":
		return False
	else:
		return True


def isWarden(request):
	user_type = request.session.get("user_type",'')
	if user_type != "warden":
		return False
	else:
		return True

def logout(request):
	request.session['login']="False";
	request.session.flush()
	return redirect('/crs/')

##This function checks that the password input in text field should not be exceeding 20 characters or less than 8 characers
#@param passwd - The password input by the user (String)
#@return boolean. True if password length is feasible else False
def validatePassword(passwd):
	return ((len(passwd) > 20) or (len(passwd) < 8))

def ApproveComplain(request):
	cid=request.session.get('currentCid')
	obj=Complain.objects.get(cid=cid)
	obj.status=0;
	obj.save();
	if request.session.get('user_type') == 'secretary':
		return redirect('/crs/listComp/')
	elif request.session.get('user_type') == 'wardenOffice':
		return redirect('/crs/listCompWardenOffice/')
	elif request.session.get('user_type') == 'warden':
		return redirect('/crs/wardenViewComplain/')
	else:
		return HttpResponse('Error')

def login(request):
	# print request.META['HTTP_HOST']
	request.session.set_expiry(0)
	try:
		if request.session.get("login") == "True": 					#check if the user is already logged in
			if request.session.get("user_type")=="student": #if yes then redirect the request to home page according to whether faculty or student
				return render_to_response('student/tables.html/', {'msg' : request.session.get('name')});
			elif request.session.get("user_type")=="warden":
				return redirect('/crs/wardenViewComplain/')
			elif request.session.get("user_type")=="secretary":
				return redirect('/crs/listComp/')
			elif request.session.get("user_type")=="wardenOffice":
				return redirect('/crs/listCompWardenOffice/')
			else:
				return redirect ('/crs/complainView/');
	except NameError:
		pass
	return render_to_response('login/loginPage.html', {'msg' : ''}, context_instance=RequestContext(request)); #if not then display the login page


def afterLogin(request):								#after login function working
	request.session.set_expiry(0)
	uname = request.POST.get('username','');
	passwd = request.POST.get('password','');
	lengthUsername = len(uname)
	if lengthUsername > 29 or lengthUsername < 1:
		return render_to_response('login/loginPage.html', {'msg':'Invalid username'}, context_instance=RequestContext(request))
	if re.search('[^a-z.@0-9]',uname):				#check username for possible SQL injection and other injections
		return render_to_response('login/loginPage.html', {'msg':'Inavlid username'}, context_instance=RequestContext(request)); #Error in username entry !!, append error message
	if validatePassword(passwd):
		return render_to_response('login/loginPage.html', {'msg':'error in password'}, context_instance=RequestContext(request)); #Error in password, append error message

	hash_object = hashlib.sha256(b""+passwd)
	passwd = hash_object.hexdigest()
	# passwd = make_password(passwd);		#Hashing/encrypting the password for further use
	if uname.endswith("fac"):
		try:
			uname = uname.replace("@fac","")
			obj=Faculty.objects.get(username=uname,password=passwd);		#username  in fac table
			request.session['login']="True";
			request.session['username']=uname;
			request.session['name'] = obj.name;
			# request.session['user_type']="faculty";
			request.session['uid']= obj.fid;
			if obj.iswarden == 2:
				request.session['user_type']="wardenOffice";
				return redirect('/crs/listCompWardenOffice/')
			elif obj.iswarden == 1:
				request.session['user_type']="warden";
				war = Warden.objects.get(fid=obj.fid)
				request.session['hostel'] = war.hostel
				return redirect('/crs/wardenViewComplain/')
			else:
				request.session['login']="False";
				request.session.flush()
				return render_to_response('login/loginPage.html', {'msg':'User not authorised.'}, context_instance=RequestContext(request))
		except:
			return render_to_response('login/loginPage.html', {'msg':'User is not registered'}, context_instance=RequestContext(request));
	elif uname.endswith("stud"):
		try:
			uname = uname.replace("@stud","")
			obj = Student.objects.get(username=uname,password=passwd);
			print str(obj)
			request.session['login']="True";
			request.session['username'] = uname;
			request.session['name'] = obj.name;
			request.session['hostel']= obj.hostel;
			request.session['uid'] = obj.uid;
			if obj.issec==1:                    
				request.session['user_type']="secretary"
				return redirect ('/crs/listComp/')
			else:
				request.session['user_type']="student"
				return redirect('/crs/complainView/')
		except:
			return render_to_response('login/loginPage.html', {'msg' : 'User is not registered'}, context_instance=RequestContext(request));
	else:
		return render_to_response('login/loginPage.html', {'msg' : 'Invalid username format'}, context_instance=RequestContext(request));


def changePasswd(request):
	if isStudent(request):
		return render_to_response('student/changePasswd.html', {'Err' : ''})
	elif isSecretary(request):
		return render_to_response('secretary/changePasswd.html', {'Err' : ''})
	elif isWardenOffice(request):
		return render_to_response('wardenOffice/changePasswd.html', {'Err' : ''})
	elif isWarden(request):
		return render_to_response('warden/changePasswd.html', {'Err' : ''})
	else:
		return redirect ('/crs/')


def resetPasswd(request):
	address = ""
	if isStudent(request):
		address = "student"
	elif isSecretary(request):
		address = "secretary"
	elif isWardenOffice(request):
		address = "wardenOffice"
	elif isWarden(request):
		address = "warden"
	else:
		return redirect ('/crs/')

	uid = request.session.get("uid")
	oldPasswd = request.POST.get('oldPasswd','')
	newPasswd = request.POST.get('newPasswd1','')
	newPasswd2 = request.POST.get('newPasswd2','')
	if validatePassword(oldPasswd) or validatePassword(newPasswd) or validatePassword(newPasswd2):
		return render_to_response(address + '/changePasswd.html', {'Err':'Password length must be between 8 & 20'})

	hash_object = hashlib.sha256(b""+oldPasswd)
	oldPasswd = hash_object.hexdigest()
	hash_object = hashlib.sha256(b""+newPasswd)
	newPasswd = hash_object.hexdigest()

	hash_object = hashlib.sha256(b""+newPasswd2)
	newPasswd2 = hash_object.hexdigest()

	if newPasswd != newPasswd2 :
		return render_to_response(address + '/changePasswd.html', {'Err' : 'Password mismatch in New Password'})
	
	if(request.session.get("user_type") == 	"student" or request.session.get("user_type") == "secretary"):
		try:
			obj = Student.objects.get(uid=uid,password=oldPasswd)
			obj.password = newPasswd
			obj.save()
		except:
			return render_to_response(address + '/changePasswd.html', {'Err' : 'old Password is Wrong!'})
	else:
		try:
			obj = Faculty.objects.get(uid=uid,password=oldPasswd)
			obj.password = newPasswd
			obj.save()
		except:
			return render_to_response(address + '/changePasswd.html', {'Err' : 'old Password is Wrong!'})
	return render_to_response('login/loginPage.html', {'Err' : 'Password changed successfully'})

def onClickForgetPassword(request):#page for entering email
	return render_to_response('login/emailPage.html')

def forgetPassword(request,token):
	return render_to_response('login/forgetPassword.html',{'token' : token})

def resettingPassword(request,token):#resetting password
	print "resetting password"
	newpassword=request.POST.get('password','')
	print newpassword
	print token
	if not (len(newpassword) > 7 and len(newpassword) < 21):
		return HttpResponse("Password Length should be between 8 and 20!")
	
	hash_object = hashlib.sha256(b""+newpassword)
	newpassword = hash_object.hexdigest()

	key=token

	# if key.endswith("5"):
	# 	if validatePassword(newpassword):
	# 		return render_to_response('student/studentHome.html',{'msg':'Invalid Password'})
	# 	else:
	# 		obj = Student.objects.get(key_value=key)
	# 		hash_object = hashlib.sha256(b""+newpassword)
	# 		passwd = hash_object.hexdigest()
	# 		obj.password=passwd
	# 		obj.save()
	# 		return HttpResponse('Password changed succeesfully')
	# elif key.endswith("0"):
	# 	if validatePassword(newpassword):
	# 		return HttpResponse('Invalid Password')
		
	# 	else:
	# 		obj = Faculty.objects.get(key_value=key)
	# 		hash_object = hashlib.sha256(b""+newpassword)
	# 		passwd = hash_object.hexdigest()
	# 		obj.password=passwd
	# 		obj.save()
	# 		return HttpResponse('Password changed successfully')
	# else:
	# 	return HttpResponse('Error in key')	
	Stud = None
	Fac = None
	try:
		Stud = Student.objects.get(key_value = token)
		Stud.key_value = ""
		Stud.password = newpassword
		Stud.save()
		return redirect('/crs/')
	except:
		print "Not Student"
		pass
	try:
		Fac = Faculty.objects.get(key_value = token)
		Fac.key_value = ""
		Fac.password = newpassword
		Fac.save()
		return redirect('/crs/')
	except:
		print "Not Faculty"
		pass

	return HttpResponse("Improper URL!")

def generateKey():
	randString = "tcxn0z2fvpydbwuqo7ils1hagjrk34e69m58"
	randtoken = ""
	for i in range(0,20):
		randtoken = randtoken + randString[randint(0,35)]
	randtoken = randtoken + str(datetime.datetime.now())
	return randtoken

def sendEmailForPassword(request):
	username=request.POST.get('username',"")
	lengthUsername = len(username)
	if lengthUsername > 29 or lengthUsername < 1:
		return HttpResponse("Invalid username")
	if re.search('[^a-z.@0-9]',username):				#check username for possible SQL injection and other injections
		return HttpResponse("Improper keys in uname")
	if username.endswith("stud"):
		username = username.replace("@stud","")
		# email=request.POST.get('email')
		obj = None
		try:
			obj=Student.objects.get(username=username);
		except:
			return HttpResponse("Improper credentials!")
		token = generateKey()
		hash_object = hashlib.sha256(b""+token)
		obj.key_value = hash_object.hexdigest()
		obj.save()
		subject="CRS : Confirmation Link For Reset Password"
		# message='The Key is' + token +'Click on the Confirmation LINK '+'http://127.0.0.1:8000/confirmationLink/';
		line1 = "Dear " + username + ",\n"
		line2 = "We received a password reset information from your CRS account at " + str((datetime.datetime.now() + timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d %H:%M:%S')) + ".\n"
		line3 = "To proceed with password reset goto the following URL : " + "http://" + request.META['HTTP_HOST'] + "/confirmationLink/" + obj.key_value + "/ \n"
		line4 = "\n\nIf the request was not generated by you, please delate this email immediately!\n\n"
		line5 = "Thank You\nCRS"
		message = line1+line2+line3+line4+line5
		print message
		print obj.email
		send_mail(subject,message,'softwareprojmanager@gmail.com',[obj.email],fail_silently=False)
		return render_to_response('login/messageSent.html')

	elif username.endswith("fac"):
		username = username.replace("@fac","")
		# email=request.POST.get('email')
		obj = None
		try:
			obj=Faculty.objects.get(username=username);
		except:
			return HttpResponse("Improper credentials!")
		token = generateKey(self)
		hash_object = hashlib.sha256(b""+token)
		obj.key_value = hash_object.hexdigest()
		obj.save()
		subject="CRS : Confirmation Link For Reset Password"
		# message='The Key is' + token +'Click on the Confirmation LINK '+'http://127.0.0.1:8000/confirmationLink/';
		line1 = "Dear " + username + ",\n"
		line2 = "We received a password reset information from your CRS account at " + str((datetime.datetime.now() + timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d %H:%M:%S')) + ".\n"
		line3 = "To proceed with password reset goto the following URL : http://127.0.0.1:8000/confirmationLink/" + obj.key_value + "/ \n"
		line4 = "\n\nIf the request was not generated by you, please delate this email immediately!\n\n"
		line5 = "Thank You\nCRS"
		message = line1+line2+line3+line4+line5
		print message
		print obj.email
		send_mail(subject,message,'softwareprojmanager@gmail.com',[obj.email],fail_silently=False)
		return render_to_response('login/messageSent.html')
	else:
		return HttpResponse("Invalid Credentials")
