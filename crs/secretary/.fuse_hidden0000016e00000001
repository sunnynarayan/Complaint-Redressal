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
from django.core import serializers
from django.core.context_processors import csrf
from django.views.decorators.csrf import requires_csrf_token
from django.core.context_processors import csrf
from student.views import *
import datetime
from datetime import timedelta
from decimal import *
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
	pubComplains = []
	priComplains = []
	try:
		pubComplains.extend(Complain.objects.raw('SELECT * FROM `complain`, complainLink WHERE (complainLink.secID = ' + str(uid) + ' AND complainLink.studID = 0) AND complain.cid = complainLink.CID AND complain.status != 21 AND complain.status != 10 AND complain.status!=0' ))
	except:
		pass
	try:
		priComplains.extend(Complain.objects.raw('SELECT * FROM `complain`, complainLink WHERE (complainLink.secID = ' + str(uid) + ' AND complainLink.studID != 0) AND complain.cid = complainLink.CID AND complain.status != 21 AND complain.status != 10 AND complain.status!=0'))
	except:
		pass	
	return render_to_response('secretary/messSecHome.html', {'public' : pubComplains, 'private' : priComplains, 'msg': request.session.get('name')});
	# return render_to_response('secretary/listComp.html',{'list' : allCom, 'msg': request.session.get('name')});

def secLodgeComplain(request):
	if not (isSecretary(request)):
		return redirect('/crs/')
	return render_to_response('secretary/secComp.html', {'msg': request.session.get('name')});

def forwardToWardenOffice(request):
	if not (isSecretary(request)):
		return redirect('/crs/')
	if 'reject' in request.POST:
		complainArray=request.POST.getlist('complain')
		length = len(complainArray)
		for x in range(0,length):
			comid = complainArray[x]
			obj=Complain.objects.get(cid=comid)
			obj.status=10
			obj.save()
	# complainObj.wardenID = wardenID
	# complainObj.save()
		return redirect('../listComp/',{'msg':'Succesfully Redirected!!!'})
	else:
		complainArray=request.POST.getlist('complain')
		length = len(complainArray)
		for x in range(0,length):
			comid = complainArray[x]
			ClO =Complainlink.objects.get(cid=comid)
			ClO.woid = "1235"
			ClO.save()
			obj=Complain.objects.get(cid=comid)
			if obj.status==1:
				obj.status=2
				time = (datetime.datetime.now() + timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d %H:%M:%S');
				obj.history = obj.history + "<br/>" + "Complain forwarded to warden office by Secretary " + request.session.get('name') + " @ : " + str(time)
				obj.save()
			elif obj.status == 11:
				obj.status = 12
				time = (datetime.datetime.now() + timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d %H:%M:%S');
				obj.history = obj.history + "<br/>" + "Complain forwarded to warden office by Secretary " + request.session.get('name') + " @ : " + str(time)
				obj.save()
		# complainObj.wardenID = wardenID
		# complainObj.save()
			return redirect('../listComp/',{'msg':'Succesfully Redirected!!!'})

def rejectComplain(request):
	if not (isSecretary(request)):
		return redirect('/crs/')
	if 'reject' in request.POST:
		complainArray=request.POST.getlist('complain')
		length = len(complainArray)
		for x in range(0,length):
			comid = complainArray[x]
			obj=Complain.objects.get(cid=comid)
			obj.status=10
			obj.save()
	# complainObj.wardenID = wardenID
	# complainObj.save()
		return redirect('../listComp/',{'msg':'Succesfully Redirected!!!'})

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

def poll(request):
	if not (isSecretary(request)):
		return redirect('/crs/')
	return render_to_response("secretary/mess/messHome.html", {'msg': request.session.get('name')})

def pollAddItem(request):
	if not (isSecretary(request)):
		return redirect('/crs/')
	return render_to_response("secretary/mess/addItem.html", {'msg': request.session.get('name')})

def addingFoodItem(request):
	if not (isSecretary(request)):
		return redirect('/crs/')
	itemName = request.POST.get('itemName')
	vitamins = request.POST.get('vitamins') 
	proteins = request.POST.get('proteins')
	fat = request.POST.get('fat')
	avgNutr = (float(vitamins) + float(proteins) + float(fat))/3
	item = Fooditems(name=itemName,vitamins=vitamins,proteins=proteins,fat=fat,nutritions=avgNutr)
	item.save()
	return redirect("/crs/pollViewItem/")

def pollViewItem(request):
	if not (isSecretary(request)):
		return redirect('/crs/')
	items = Fooditems.objects.all()
	return render_to_response("secretary/mess/viewItem.html", {'list': items , 'msg': request.session.get('name')})

def pollMakeMeal(request):
	if not (isSecretary(request)):
		return redirect('/crs/')
	# items = Fooditems.objects.raw("SELECT * FROM foodItems ORDER BY FID")
	items = Fooditems.objects.all().order_by('fid')
	item = []
	name = []
	nutrition = []
	for x in items:
		item.append(int(x.fid))
		name.append(str(x.name))
		nutrition.append(x.nutritions)
	request.session['Messitem'] = item
	request.session['Messname'] = name
	request.session['Messnutrition'] = nutrition
	return render_to_response("secretary/mess/makeMeal.html", {'list': items , 'msg': request.session.get('name')})


def makingMeal(request):
	if not (isSecretary(request)):
		return redirect('/crs/')
	itemIndex=request.POST.getlist('foodItems')
	itemIndex.sort();
	items = request.session.get('Messitem')
	name = request.session.get('Messname')
	nutrition = request.session.get('Messnutrition')
	length = len(itemIndex)
	if (length == 0):
		return redirect('/crs/pollMakeMeal/')
	Fid = []
	makeFid = str(items[int(itemIndex[0]) - 1])
	Fid.append(str(items[int(itemIndex[0]) - 1]))
	# makeName = str(name[int(itemIndex[0]) - 1])
	# makeNutrition = nutrition[int(itemIndex[0]) - 1]
	for x in range(1,length):
		makeFid = makeFid + "," + str(items[int(itemIndex[x]) - 1])
		Fid.append(str(items[int(itemIndex[x]) - 1]))
		# makeName = makeName + "," + str(name[int(itemIndex[x]) - 1])
		# makeNutrition = makeNutrition + nutrition[int(itemIndex[x]) - 1]

	# makeNutrition = makeNutrition / length
	try:
		Meal = Meals(fid = makeFid, items=length)
		Meal.save()
		Meal = Meals.objects.get(fid = makeFid)
		mid = Meal.mid
		for fid in Fid:
			mealLink = Mealitems(mid=mid, fid=fid)
			mealLink.save()
	except:
		return redirect('/crs/pollMakeMeal/')
	return redirect('/crs/viewMeal/')

class MealItems:
	def __init__(self , MID):
		self.mid = MID
		self.FoodItems = []
		self.protein = 0.0
		self.vitamin = 0.0
		self.fat = 0.0
		self.PopulateFid()
		self.avgnutrition = float((self.fat + self.protein + self.fat)/3)
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
		self.protein = float(self.protein/len(mealItems))
		self.vitamin = float(self.vitamin/len(mealItems))
		self.fat = float(self.fat /len(mealItems))

def viewMeal(request):
	if not (isSecretary(request)):
		return redirect('/crs/')
	print "Secretary!"
	# PlayerStats.objects.all().select_related('player__positionstats')
	if checkAvailabilityOfPoll(int(request.session.get('hostel'))):
		return redirect('/crs/pollResult/')
	mealItems = []
	mls = Meals.objects.all()
	for meal in mls:
		x = MealItems( meal.mid )
		mealItems.append(x)


	MealList = []
	for meal in mealItems:
		MealList.append(int(meal.mid))

	request.session['mealList'] = MealList
	foodItems = Fooditems.objects.all()

	return render_to_response("secretary/mess/viewMeal.html", {'list' : mealItems , 'msg': request.session.get('name')})

def addItemToPoll(request):
	if not (isSecretary(request)):
		return redirect('/crs/')
	if checkAvailabilityOfPoll(int(request.session.get('hostel'))):
		return redirect('/crs/')
	# redirect to page that shows that no poll is available!
	breakfastItems = request.POST.getlist('breakfast')
	lunchItems = request.POST.getlist('lunch')
	dinnerItems = request.POST.getlist('dinner')
	mealList = request.session.get('mealList')
	mealItems = []
	for x in mealList:
		mealItems.append(MealItems(x))

	pollMenuItem = []
	if len(breakfastItems) > 0:
		for breakfast in breakfastItems:
			if int(breakfast) < 1 or int(breakfast) > len(mealList):
				return redirect('/crs/viewMeal/')
			pollMenuItem.append(Pollmenu(hostel=request.session.get('hostel'),meal = mealItems[int(breakfast)-1].name,type=1, protein = mealItems[int(breakfast)-1].protein, vitamin = mealItems[int(breakfast)-1].vitamin, fat = mealItems[int(breakfast)-1].fat, nutritions = mealItems[int(breakfast)-1].avgnutrition))
	if len(lunchItems) > 0:
		for lunch in lunchItems:
			if int(lunch) < 1 or int(lunch) > len(mealList):
				return redirect('/crs/viewMeal/')
			pollMenuItem.append(Pollmenu(hostel=request.session.get('hostel') ,meal = mealItems[int(lunch)-1].name,type=2, protein = mealItems[int(lunch)-1].protein, vitamin = mealItems[int(lunch)-1].vitamin, fat = mealItems[int(lunch)-1].fat, nutritions = mealItems[int(lunch)-1].avgnutrition))

	if len(dinnerItems) > 0:
		for dinner in dinnerItems:
			if int(dinner) < 1 or int(dinner) > len(mealList):
				return redirect('/crs/viewMeal/')
			pollMenuItem.append(Pollmenu(hostel=request.session.get('hostel') ,meal = mealItems[int(dinner)-1].name,type=3, vitamin = mealItems[int(dinner)-1].vitamin, protein = mealItems[int(dinner)-1].protein, fat = mealItems[int(dinner)-1].fat, nutritions = mealItems[int(dinner)-1].avgnutrition))

	for item in pollMenuItem:
		item.save()
	return redirect('/crs/viewMeal/')

def searchDatabase(request):
	return render_to_response ("secretary/search.html", context_instance=RequestContext(request))

def validateTypeOfSearch(argument):
	try:
		if int(argument)>0 and int(argument)<6:
			return True
		else:
			return False
	except:
		return False

def validateParameter(parameter, sequence):
	if sequence == "1":
		if re.search('^[A-Z]{2}-[A-Z]{2}-\d{2}/\d{2}/\d{2}-\d{4}$', parameter):
			return True
	elif sequence == "2":
		if re.search('^[A-Za-z]*$', parameter) and (len(parameter) > 0 and  len(parameter) < 51):
			return True
	elif sequence == "3":
		if re.search('^\d{4}-\d{2}-\d{2}$', parameter):
			return True
	elif sequence == "4" or sequence == "5":
		return True
	return False

def searchItem(request):
	# search type details : 
	# 1 - search by complainID
	# 2 - search by student's Name
	# 3 - search by lodge date
	# 4 - search by subject
	# 5 - search by detail
	typeOfSearch = str(request.POST.get('type',''))
	if not validateTypeOfSearch(typeOfSearch):
		return redirect ('/crs/search/') 								#redirect to search page
	parameter = str(request.POST.get('parameter',''))
	if not validateParameter(parameter, typeOfSearch):
		return redirect('/crs/search')
	complain = []
	if typeOfSearch == '1':
		try:
			complain.extend(Complain.objects.filter(cid=parameter))
		except:
			pass

	elif typeOfSearch == '2':
		try:
			student = Student.objects.filter(name__icontains=parameter)
			for stud in student:
				complain.extend(Complain.objects.filter(uid = stud.uid))
		except:
			pass

	elif typeOfSearch == '3':
		try:
			complain.extend(Complain.objects.filter(time__icontains=parameter))
		except:
			pass
		
	elif typeOfSearch == '4':
		parameter = validateText(parameter)
		try:
			complain.extend(Complain.objects.filter(subject__icontains=parameter))
		except:
			pass
		
	else:
		parameter = validateText(parameter)
		try:
			complain.extend(Complain.objects.filter(detail__icontains=parameter))
		except:
			pass

	return render_to_response("secretary/searchResult.html", {'list' : complain})

def endPoll(self):
	#check if request came from secretary or not
	if not (isSecretary(request)):
		return redirect('/crs/')
	#check if request came from genuine mess secretary or not.
	#check availability of polling fot this hostel
	if not checkAvailabilityOfPoll(int(request.session.get('hostel'))):
		return HttpResponse('No polling available')
	#if polling is available then proceed
	Pollresult.objects.filter(hostel = request.session.get('hostel')).delete()
	#delete any existing poll result from the result table!
	breakfastPollOptions = []
	lunchPollOptions = []
	dinnerPollOptions = []
	votesB = []
	votesL = []
	votesD = []
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
			# dataB = dataB + "B-Item " + str(b) + "\t" + str(Pollvoting.objects.filter(id=x.id).count()) + "\n"
			# b = b + 1
		except:
			votesB.append(PollMenuVoting(x,0))
			# dataB = dataB + "B-Item " + str(b) + "\t0\n"
			# b = b + 1
	for x in lunchPollOptions:
		try:
			votesL.append(PollMenuVoting(x,Pollvoting.objects.filter(id=x.id).count()))
			# dataL = dataL + "L-Item " + str(l) + "\t" + str(Pollvoting.objects.filter(id=x.id).count()) + "\n"
			# l = l + 1
		except:
			votesL.append(PollMenuVoting(x,0))
			# dataL = dataL + "L-Item " + str(l) + "\t0\n"
			# l = l + 1
	for x in dinnerPollOptions:
		try:
			votesD.append(PollMenuVoting(x,Pollvoting.objects.filter(id=x.id).count()))
			# dataD = dataD + "D-Item " + str(d) + "\t" + str(Pollvoting.objects.filter(id=x.id).count()) + "\n"
			# d = d + 1
		except:
			votesD.append(PollMenuVoting(x,0))
			# dataD = dataD + "D-Item " + str(d) + "\t0\n"
			# d = d + 1

	#Now add things to the result table!
	PollresultArray = []

	for x in votesB:
		PollresultArray.append(Pollresult(hostel=request.session.get('hostel'),type=1,meal=x.meal,vote=x.votes,protein=x.protein,vitamin=x.vitamin,fat=x.fat,nutritions=x.nutritions))
	for x in votesL:
		PollresultArray.append(Pollresult(hostel=request.session.get('hostel'),type=2,meal=x.meal,vote=x.votes,protein=x.protein,vitamin=x.vitamin,fat=x.fat,nutritions=x.nutritions))
	for x in votesD:
		PollresultArray.append(Pollresult(hostel=request.session.get('hostel'),type=3,meal=x.meal,vote=x.votes,protein=x.protein,vitamin=x.vitamin,fat=x.fat,nutritions=x.nutritions))

	#Then remove things from polling table!

	for x in breakfastPollOptions:
		Pollvoting.objects.filter(id=x.id).delete()
		x.delete()

	for x in lunchPollOptions:
		Pollvoting.objects.filter(id=x.id).delete()
		x.delete()

	for x in dinnerPollOptions:
		Pollvoting.objects.filter(id=x.id).delete()
		x.delete()

	#Finally pollMenu has been freed again and result has been stored in pollResult

	#Now redirect the page to the poll result page!

	return HttpResponse('later on page will be Redirected for final polling result page!')

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
