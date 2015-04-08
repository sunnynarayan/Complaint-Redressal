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
from reportlab.pdfgen import canvas
from reportlab.platypus import Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import landscape
from django.core.context_processors import csrf
from django.views.decorators.csrf import requires_csrf_token
from django.core.context_processors import csrf
from student.views import validateText
import datetime
from datetime import timedelta

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
		pubComplains.extend(Complain.objects.raw('SELECT * FROM `complain`, complainLink WHERE (complainLink.secID = ' + str(uid) + ' AND complainLink.studID = 0) AND complain.cid = complainLink.CID'))
	except:
		pass
	try:
		priComplains.extend(Complain.objects.raw('SELECT * FROM `complain`, complainLink WHERE (complainLink.secID = ' + str(uid) + ' AND complainLink.studID != 0) AND complain.cid = complainLink.CID'))
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
			obj.history = obj.history + "<br/>" + "Re-lodged Complain forwarded to warden office by Secretary " + request.session.get('name') + " @ : " + str(time)
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
		obj=Complain.objects.get(cid=comid)
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
    return render_to_response("secretary/complainDetail.html", {'item': complainObject[0]})

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
    	self.protein = 0
    	self.vitamin = 0
    	self.fat = 0
    	self.PopulateFid()
    	self.name = ""
    	for fobj in self.FoodItems:
    		self.name = self.name + fobj.name + ","

    def PopulateFid(self):
    	mealItems = Mealitems.objects.filter(mid = self.mid)
    	for mi in mealItems:
    		fitem = Fooditems.objects.get(fid=mi.fid)
    		self.FoodItems.append(fitem)
    		self.protein = self.protein + 1
    		self.vitamin = self.vitamin + 1
    		self.fat = self.fat + 1

def viewMeal(request):
	if not (isSecretary(request)):
		return redirect('/crs/')
	# PlayerStats.objects.all().select_related('player__positionstats')
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
	breakfastItems = request.POST.getlist('breakfast')
	lunchItems = request.POST.getlist('lunch')
	dinnerItems = request.POST.getlist('dinner')
	mealList = request.session.get('mealList')
	for x in mealList:
		mealItems.append(MealItems(x))

	pollMenuItem = []
	if len(breakfastItems) > 0:
		for breakfast in breakfastItems:
			if int(breakfast) < 1 or int(breakfast) > len(mealList):
				return redirect('/crs/viewMeal/')
			pollMenuItem.append(Pollmenu(hostel=request.session.get('hostel'),meal = mealItems[int(breakfast)-1].name,type=1, protein = mealItems[int(breakfast)-1].protein, vitamin = mealItems[int(breakfast)-1].vitamin, fat = mealItems[int(breakfast)-1].fat))
	if len(lunchItems) > 0:
		for lunch in lunchItems:
			if int(lunch) < 1 or int(lunch) > len(mealList):
				return redirect('/crs/viewMeal/')
			pollMenuItem.append(Pollmenu(hostel=request.session.get('hostel') ,meal = mealItems[int(lunch)-1].name,type=2, protein = mealItems[int(lunch)-1].protein, vitamin = mealItems[int(lunch)-1].vitamin, fat = mealItems[int(lunch)-1].fat))

	if len(dinnerItems) > 0:
		for dinner in dinnerItems:
			if int(dinner) < 1 or int(dinner) > len(mealList):
				return redirect('/crs/viewMeal/')
			pollMenuItem.append(Pollmenu(hostel=request.session.get('hostel') ,meal = mealItems[int(dinner)-1].name,type=3, vitamin = mealItems[int(dinner)-1].vitamin, protein = mealItems[int(dinner)-1].protein, fat = mealItems[int(dinner)-1].fat))

	for item in pollMenuItem:
		item.save()
	return redirect('/crs/viewMeal/')

def viewPollOptions(request):
	if not (isSecretary(request)):
		return redirect('/crs/')
	qryBreakfast = "SELECT b.MID, b.name, b.avgNutrition FROM pollMenu a, meals b WHERE a.hostel = " + str(request.session.get('hostel')) +" AND a.type = 1 AND a.MID = b.MID"
	qryLunch = "SELECT b.MID, b.name, b.avgNutrition FROM pollMenu a, meals b WHERE a.hostel = " + str(request.session.get('hostel')) +" AND a.type = 2 AND a.MID = b.MID"
	qryDinner = "SELECT b.MID, b.name, b.avgNutrition FROM pollMenu a, meals b WHERE a.hostel = " + str(request.session.get('hostel')) +" AND a.type = 3 AND a.MID = b.MID"
	breakfastItems = Meals.objects.raw(qryBreakfast)
	lunchItems = Meals.objects.raw(qryLunch)
	dinnerItems = Meals.objects.raw(qryDinner)	
	return render_to_response("secretary/mess/viewMenu.html", {'list1' : breakfastItems, 'list2' : lunchItems, 'list3' : dinnerItems, 'msg': request.session.get('name')})


from django.http import HttpResponse

def some_view(request):
	# Create the HttpResponse object with the appropriate PDF headers.
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'filename="experiment.pdf";pagesize=landscape(letter)'

	# Create the PDF object, using the response object as its "file."
	p = canvas.Canvas(response)
	p.setFont('Helvetica', 48, leading=None)
	p.drawCentredString(300, 750, "Warden's Office")

	p.setFont('Helvetica', 25, leading=None)
	p.drawCentredString(300, 700, "Hostel Leaving Form")
	
	line1 = "I " + request.session.get('name')
	line2 = "staying presently in Room No 209" 
	line3 = "of Ashoka Hall"
	line4 = "do hereby intimate that I am leaving hostel"

	# p.drawImage('sm_logo.png', 100, 100, width=None, height=None)
	p.setFont('Helvetica', 25, leading=None)
	p.drawString(50, 600, line1)
	p.setFont('Helvetica', 25, leading=None)
	p.drawString(50, 550, line2)
	p.setFont('Helvetica', 25, leading=None)
	p.drawString(50, 500, line3)
	# Draw things on the PDF. Here's where the PDF generation happens.
	# See the ReportLab documentation for the full list of functionality.
	
	# Close the PDF object cleanly, and we're done.
	p.showPage()
	p.save()
	return response

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
