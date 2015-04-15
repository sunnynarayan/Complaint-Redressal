import operator
import datetime
import time
from login.models import *

class Temporary:
	
    def __init__(self,cid,time,populate,length):
    	self.cid=cid
    	self.time=time
    	self.populate=populate
        self.length=length
        weight=time+populate
        priority=length/weight

def getLJ(comp):
	if comp == 1:
		return 3;
	elif comp == 2:
		return 2;
	elif comp == 3:
		return 1;
	elif comp == 4:
		return 1;
	else:
		return 2

def Schedule(request):
	print "hello"
	uid=request.session.get('uid')		
	# PublicComplainObjects = Complainlink.objects.all().filter(wardenid = uid).filter(studid = 0);
	query1 = 'SELECT * FROM `complain`, complainLink WHERE (complain.status = 3 OR complain.status = 13 OR complain.status = 23) AND (complainLink.wardenid = ' + str(uid) + ' AND complainLink.studID = 0) AND complain.cid = complainLink.CID ORDER BY complain.time ASC'
	PublicComplainObjects = Complainlink.objects.raw(query1)
	query2 = 'SELECT * FROM `complain`, complainLink WHERE (complain.status = 3 OR complain.status =  13 OR complain.status = 23) AND (complainLink.wardenid = ' + str(uid) + ' AND complainLink.studID != 0) AND complain.cid = complainLink.CID ORDER BY complain.time ASC'
	PrivateComplainObjects = Complainlink.objects.raw(query2)
	# PrivateComplainObjects=Complainlink.objects.all().filter(wardenid = uid).exclude(studid = 0);
	Public_List=[];
	Private_List=[];
	Time_List1=time_calculate(PublicComplainObjects);
	Populate_List=populate_calculate(PublicComplainObjects);
	count = 0
	print "About to enter loop for pub complain"
	print str(len(Populate_List))
	print str(len(Time_List1))
	for x in PublicComplainObjects:
		Public_List.append(Temporary(x.cid, Time_List1[count], Populate_List[count], getLJ(x.type)))
		count = count + 1
	
	Time_List1=time_calculate(PrivateComplainObjects);
	Populate_List=populate_calculate(PrivateComplainObjects);
	cnt = 0
	print "About to enter loop for pri complain"
	print str(len(Populate_List))
	print str(len(Time_List1))
	for x in PrivateComplainObjects:
		Private_List.append(Temporary(x.cid,Time_List1[cnt], Populate_List[cnt],getLJ(x.type)))
		cnt = cnt + 1
    
	Public_List.sort(key = operator.attrgetter('priority'));
	Private_List.sort(key = operator.attrgetter('priority'));
	return render_to_response('warden/wardenViewComplain.html',{'list1' : Public_List, 'list2': Private_List})

def time_calculate(List):
	Time_List1=[];
	s= str(List[0].time)
	base_time= int(datetime.datetime(int(s[0:4]),int(s[5:7]),int(s[8:10]),int(s[11:13]),int(s[14:16]),int(s[17:19])).strftime('%s'))
	print str(base_time)
	seconds = int(round(time.time())) + 19800
	print str(seconds)
	base= seconds-base_time;
	for x in List :
		s1 = str(x.time)
		complain_time=int(datetime.datetime(int(s1[0:4]),int(s1[5:7]),int(s1[8:10]),int(s1[11:13]),int(s1[14:16]),int(s1[17:19])).strftime('%s'))
		seconds1 = int(round(time.time())) + 19800
		base1= seconds1-complain_time;
		Time_List1.append(base1/base);

	return Time_List1;

def populate_calculate(List):
	Populate_List=[];
	count1,count2,count3,count4 = 0,0,0,0
	for x in List:
		print "print from populate_calculate" + str(x)
		complain_type=x.type;
		if(complain_type==1):
			count1 = count1 + 1
		elif(complain_type==2):
			count2 = count2 + 1
		elif(complain_type==3):
			count3 = count3 + 1
		else:
			count4 = count4 + 1
	foo = [count1,count2,count3,count4];
	base= max(foo);
	print str(base)
	print "Starting to append the list"
	for xx in List:
		complain_type=xx.type
		print str(xx)
		print "complain_type =" + str(complain_type)
		print str(complain_type == 2)
        if complain_type == 1:
        	print "Appended for count 1"
        	Populate_List.append(count1/base)
        elif complain_type == 2:
        	print "Appended for count 2"
        	Populate_List.append(count2/base)
        elif complain_type == 3:
        	print "Appended for count 3"
        	Populate_List.append(count3/base)
        elif complain_type == 4:
        	print "Appended for count 4"
        	Populate_List.append(count4/base)
        else:
        	print "else"
        	pass
        print "done"
	return Populate_List;