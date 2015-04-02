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
	return render_to_response('secretary/listComp.html',{'public' : pubComplains, 'private' : priComplains, 'msg': request.session.get('name')});
	# return render_to_response('secretary/listComp.html',{'list' : allCom, 'msg': request.session.get('name')});

def secLodgeComplain(request):
	if not (isSecretary(request)):
		return redirect('/crs/')
	return render_to_response('secretary/secComp.html');

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
	return render_to_response("secretary/mess/messhome.html", {'msg': request.session.get('name')})

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
	avgNutr = (int(vitamins) + int(proteins) + int(fat))/3
	item = Fooditems(name=itemName,vitamins=vitamins,proteins=proteins,fat=fat,nutritions=avgNutr)
	item.save()
	return redirect("/crs/pollViewItem/")

def pollViewItem(request):
	if not (isSecretary(request)):
		return redirect('/crs/')
	items = Fooditems.objects.raw("SELECT * FROM foodItems")
	return render_to_response("secretary/mess/viewItem.html", {'list': items })

def pollMakeMeal(request):
	if not (isSecretary(request)):
		return redirect('/crs/')
	items = Fooditems.objects.raw("SELECT * FROM foodItems ORDER BY FID")
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
	return render_to_response("secretary/mess/makeMeal.html", {'list': items })


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

	makeFid = str(items[int(itemIndex[0]) - 1])
	makeName = str(name[int(itemIndex[0]) - 1])
	makeNutrition = nutrition[int(itemIndex[0]) - 1]
	for x in range(1,length):
		makeFid = makeFid + "," + str(items[int(itemIndex[x]) - 1])
		makeName = makeName + "," + str(name[int(itemIndex[x]) - 1])
		makeNutrition = makeNutrition + nutrition[int(itemIndex[x]) - 1]

	makeNutrition = makeNutrition / length

	Meal = Meals(fid = makeFid, name = makeName, avgnutrition = makeNutrition)
	Meal.save()
	return redirect('/crs/viewMeal/')

def viewMeal(request):
	if not (isSecretary(request)):
		return redirect('/crs/')
	items = Meals.objects.all()
	MealList = []
	for meal in items:
		MealList.append(int(meal.mid))
	request.session['mealList'] = MealList
	return render_to_response("secretary/mess/viewMeal.html", {'list' : items})

def addItemToPoll(request):
	if not (isSecretary(request)):
		return redirect('/crs/')
	breakfastItems = request.POST.getlist('breakfast')
	lunchItems = request.POST.getlist('lunch')
	dinnerItems = request.POST.getlist('dinner')
	mealList = request.session.get('mealList')
	pollMenuItem = []
	if len(breakfastItems) > 0:
		for breakfast in breakfastItems:
			if int(breakfast) < 1 or int(breakfast) > len(mealList):
				return redirect('/crs/viewMeal/')
			pollMenuItem.append(Pollmenu(hostel=request.session.get('hostel') ,mid= mealList[int(breakfast)-1],type=1))
	if len(lunchItems) > 0:
		for lunch in lunchItems:
			if int(lunch) < 1 or int(lunch) > len(mealList):
				return redirect('/crs/viewMeal/')
			pollMenuItem.append(Pollmenu(hostel=request.session.get('hostel') ,mid= mealList[int(lunch)-1],type=2))

	if len(dinnerItems) > 0:
		for dinner in dinnerItems:
			if int(dinner) < 1 or int(dinner) > len(mealList):
				return redirect('/crs/viewMeal/')
			pollMenuItem.append(Pollmenu(hostel=request.session.get('hostel') ,mid= mealList[int(dinner)-1],type=3))

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
	return render_to_response("secretary/mess/viewMenu.html", {'list1' : breakfastItems, 'list2' : lunchItems, 'list3' : dinnerItems})


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
def editProfile(request):
	return redirect('//')

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
	# elif sequence == "4":
		# if re.search('')
	# elif sequence == "5":
		# if re.search('')

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
		# return render_to_response("281")
	parameter = str(request.POST.get('parameter',''))
	# if not validateParameter(parameter, typeOfSearch):
		# return redirect('/crs/search')
		# return render_to_response("285")
	if typeOfSearch == '1':
		complain = Complain.objects.raw('SELECT * FROM complain WHERE cid = ' + parameter)
		return render_to_response("secretary/searchResult.html", {'list' : complain})
	elif typeOfSearch == '2':
		complain = []
		# try:
		student = Student.objects.filter(name__icontains=parameter)
		for stud in student:
			complain.extend(Complain.objects.filter(uid = stud.uid))
		# except:
			# pass
		return render_to_response("secretary/searchResult.html", {'list' : complain})
	elif typeOfSearch == '3':
		complain = Complain.objects.raw('SELECT * FROM complain WHERE time LIKE \'' + parameter + '%\'')
		return render_to_response("secretary/searchResult.html", {'list' : complain})
	# elif typeOfSearch == '4':
	# 	pass
	# elif typeOfSearch == '5':
	# 	pass