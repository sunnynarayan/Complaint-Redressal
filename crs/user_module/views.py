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
from user_module.models import Faculty
from user_module.models import Student
# from django.contrib.auth.hashers import make_password
# from django.contrib.auth.hashers import make_password

#module for SHA256
import re  #for reagex functions
# def ankt(request):
# 	abc = "mypassword"
# 	hash_object = hashlib.sha256(b""+abc)
# 	hex_dig = hash_object.hexdigest()
# 	return render_to_response('user_module/untitled.html',{'ankit_chu':hex_dig});

def getSecretaryType(str):
	if str=='eco':
		return 0;
	elif str=='mess':
		return 1;
	elif str=='maintenance':
		return 2;
	elif str=='tech':
		return 3;

def	getComplaintType(str):
	if str=='private':
		return 1;
	else:
		return 0; 

def getHostel(str):
	if str=='Ashoka':
		return 0;
	elif str=='Aryabhatta':
		return 1;
	elif str=='Chanakya1':
		return 2;
	elif str=='Chanakya2':
		return 3;
	else:
		return 4;


def login(request):
	try:
		if request.session.get("login") == "True":							#check if the user is already logged in
			if request.session.get("user_type")=="faculty" :		#if yes then redirect the request to home page according to whether faculty or student
				return render_to_response('user_module/wardenViewComplain.html');
			else:
				return render_to_response('user_module/studentBase.html');
	except NameError:
		return render_to_response('user_module/loginPage.html', {'msg':''});	

	return render_to_response('user_module/loginPage.html', {'msg':''});		#if not then display the login page

def afterLogin(request):#after login function working
	uname = request.POST.get('username','');
	passwd = request.POST.get('password','');
	if re.sub('[a-z.@0-9]',"",uname) != "":				#check username for possible SQL injection and other injections
		return render_to_response('user_module/loginPage.html', {'msg':'Errornous user'}); #Error in username entry !!, append error message
	if (len(passwd) > 20) or (len(passwd) < 8):
		return render_to_response('user_module/loginPage.html', {'msg':'error in password'}); #Error in password, append error message

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
			# request.set_cookie['max_age']=60000;
			return render_to_response('user_module/wardenViewComplain.html');
		except:
			return render_to_response('user_module/loginPage.html', {'msg':'invalid user: '+uname + 'password : ' + passwd});
	elif uname.endswith("stud"):
		try:
			uname = uname.replace("@stud","")
			obj=Student.objects.get(username=uname,password=passwd);	#username  in stud table
			request.session['login']="True";
			request.session['username']=uname;
			name = obj.name;
			# 	request.set_cookie['max_age']=60000;
			request.session['user_type']="student";
			return render_to_response('user_module/studentBase.html', {'msg':name});
		except:
			return render_to_response('user_module/loginPage.html', {'msg' : 'unknown user : ' + uname + "pass : " + passwd});
	else:
		return render_to_response('user_module/loginPage.html', {'msg' : 'username recieved : ' + uname + "pass : " + passwd});

def studentComplainView(request):
	return render_to_response('users/viewStudComplain.html');


def viewComplaints(request):
	if request.session['is_logged']==True:
		objects1=Complaint.objects.all().filter(complainttype=0);#0 for priate complaint
		objects2=Complaints.objects.all().filter(complainttype=1);#1 for public complaint complaint
		return render_to_response('users/view_complaint.html',{'lists1':objects1},{'lists2':objects2});#sending two objects list to the html pages
	else:
		return render_to_response('users/invalidlogin.html');
def lodgeComplaints(request):
	if request.session['is_logged']==True and request.session['user_type']==student:
		subject=request.Post['subject'];
		detail=request.Post['message'];
		comment=request.Post['comment'];
		bypass=0;
		hostel=function_togthostel(request.Post['hostel']);
		time=datetime.datetime.now();
		Uid=request.session['username'];
		sec_type=getSecretaryType(request.Post['Secretary']);
		complaint_type=getComplaintType(request.Post['com_type']);
		complnobj=complaint(UID=uid,time=time,hostel=hostel,type1=sec_type,type2=complaint_type,subject=subject,detail=detail,comment=comment,bypass=0);


	else:
		return render_to_response('users/invalidlogin.html');

def editProfile(request):
	if request.session['is_logged']==True and request.session['user_type']==student:
		mobile=request.Post['mobile'];
		bAccNo=request.Post['bankacc'];
		bank=request.Post['bank'];
		email=request.Post['email'];
		ifsc=request.Post['ifsc'];
		if len(mobile)!=10:
			return render_to_response('users/invalidlogin.html',{msg:'Your mobile number must be 10 digits only'});
		if len(ifsc)!=11:
			return render_to_response('users/invalidlogin.html',{msg:'Your IFSC code must be 11 digits long'});
		if len(bAccNo)!=18:
			return render_to_response('users/invalidlogin.html',{msg:'Your Account Number number must be 18 digits only'});
		try:
			obj=Student.objects.get(request.session['user']);
			obj.mobile=mobile;
			obj.bAccNo=bAccNo;
			obj.bank=bank;
			obj.ifsc=ifsc;
			obj.email=email;
			obj.save();
			return render_to_response('users/saved_credentials.html');
		except:
			return render_to_response('users/invalid.html',{msg:'Error_User_doesnExists'});
	elif request.session['is_logged']==True and request.session['user_type']==faculty:
		mobile=request.Post['mobile'];
		if len(mobile)!=10:
			return render_to_response('users/invalidlogin.html',{msg:'Your mobile number must be 10 digits only'});
		try:
			obj=Faculty.objects.get(request.session['user']);
			obj.mobile=mobile;
			obj.save();
			return render_to_response('users/saved_credentials_for_faculty.html')
		except:
			return render_to_response('users/invalid.html',{msg:'Error_User_doesnExists'});
	else:
		render_to_response('users/invalidlogin.html');


		

# def trackStatus(request):
# 	if request.session['is_logged']==True and request.session['user_type']==student:
		
def rateSecretary(request):
	if request.session['is_logged']==True and request.session['user_type']==student:
		rating=request.Post['rating'];
		sec_rated=request.Post['rating'];
		try:
			obj=Secretary.objects.get(SID=sec_rated);
			obj.rating=rating;#saving the rating in secretary table
			obj.save();
		except:

			render_to_response('users/invalidlogin.html');
	else:
		render_to_response('users/invalidlogin.html');

def hostelLeavingInfo(request):
	if request.session.get('is_logged')==True and request.session('user_type')==student:
		username=request.session['username'];
		obj=Student.objects.get(username=username);
		hostel=obj.hostel;



def RatingsAndComments(request):
	if request.session['is_logged']==True and request.session['user_type']==student:
		objects1=Secretary.objects.all().filter(SID=0);
		objects2=Secretary.objects.all().filter(SID=1);
		objects3=Secretary.objects.all().filter(SID=2);
		objects4=Secretary.objects.all().filter(SID=3);
		name1=objects1.UID.username;
		rating1=objects1.rating;
		name2=objects2.UID.username;
		rating2=objects2.rating;
		name3=objects3.UID.username;
		rating3=objects3.rating;
		name4=objects4.UID.username;
		rating4=objects4.rating;
	if 'Add User' in request.POST:
		try:
			obj=User.objects.get(username=username)
			return render_to_response('users/login.html',{'msg':Error_User_Exists})
		except:			
			if  len(username)==0 or len(username)>128:
			 	return render_to_response('users/login.html',{'msg':Error_Bad_Username})
          		
       			elif len(passwd) != 5 and len(passwd) != 0:
				return render_to_response('users/login.html',{'msg':Error_Bad_Password})
			else:
				q=User(username=request.POST['username'],password=request.POST['password']);
				q.save();
				return render_to_response('users/welcome.html',{'username':q.username})						
   	elif  'Login' in request.POST:
		user = authenticate(username=username, password=passwd)
		if user is not None:
        		if user.is_active:
            			login(request, user)
            			return render_to_response('users/welcome.html',{'username':user.username})
        		else:
				return render_to_response('users/login.html',{'msg':Error_Bad_Credentials})

            # Return a 'disabled account' error message
		else:
			return render_to_response('users/login.html',{'msg':Error_Bad_Credentials})
        # Return an 'invalid login' error message.
	
			
									
   	else:
        	raise Http404()