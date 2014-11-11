from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth import login as User
from django.contrib.auth import authenticate, login
from django.core.context_processors import csrf
import json
import smtplib
from leaveform.models import user_leave
from leaveform.models import Leave_status
from leaveform.models import new_user
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import date
from django.core.mail import send_mail, EmailMultiAlternatives
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.contrib.auth.models import User
from requests import Request, Session
from django.template.loader import render_to_string


def main(request):
	return render(request,'main.html')



def signup(request):
	return render(request,'signup.html')



def loginpage(request):
	return render(request,'login.html')



def createaccount(request):
	if request.method == 'POST':
		post, data, req_field = request.POST, {}, ['username' ,'password','gender','dob','mail','mob']
		for i in req_field:
			data[i] = post['all[%s]'%i]
		auth = User.objects.create_user(data['username'],'',data['password'])
		available_leave=12
		new_user.objects.create(
                                    Available_leave=available_leave,
                                    username = data['username'],
                                    password=data['password'],
                                    gender=data['gender'],
                                    dob=data['dob'],
                                    mail = data['mail'],
                                    mob = data['mob'], 
                                    auth=auth,
                                    )
        dump="saved"
        return HttpResponse(content=json.dumps(dump),content_type='Application/json')
        return render(request,'signup.html')



def approverlogin(request):
	if request.method=='POST':
		username=request.POST['username']
		password=request.POST['password']
		user=authenticate(username=username,password=password)
		print user
		if user.is_superuser:
			dump="success"
		return HttpResponse(content=json.dumps(dump),content_type='Application/json')
	return render(request,'approverlogin.html')
    


def login_check(request):
	username=request.POST['username']
	password=request.POST['password']
	user=authenticate(username=username,password=password)
	if user:
		login(request,user)
		dump="success"
		return HttpResponse(content=json.dumps(dump),content_type='Application/json')
	else:
		login(request,'login.html')



def home(request):
	data = []
	temp={}
	if request.method=='POST':
		post=request.POST
		datadump=new_user.objects.all()
		for i in datadump:
			data.append({'Available_leave':i.Available_leave})
			print data
			return HttpResponse(content=json.dumps({'data':data}),content_type='Application/json')
	return render(request, 'home.html')
def logout_view(request):
	logout(request)
	return render(request,'login.html')



def leaveform(request):
	data =[]
	dat=str(request.user)
	if request.method == 'POST':
		# print "dkashdjkhasdkhakjdhkjadsh"
		post, data, req_field = request.POST, {}, ['leavetype' ,'From_date','To_date','Timeoff','WDapply','remark']
		for i in req_field:
			data[i] = post['all[%s]'%i]
		print 'insidepost'
		user_leave.objects.create( 
									user=dat,
                                    leave_type = data['leavetype'],
                                    From_date=data['From_date'],
                                    To_date=data['To_date'],
                                    Timeoff=data['Timeoff'],
                                    WDay_apply = data['WDapply'],
                                    Remarks = data['remark'], 
                                    )
		currentuser=str(request.user)
		print currentuser
		dump ='saved'
		send_message_to_user(currentuser,data['leavetype'],data['From_date'],data['To_date'],data['Timeoff'],data['WDapply'],data['remark']); #dat, data['Timeoff'],data['remark'])
		return HttpResponse(content=json.dumps(dump),content_type='Application/json')
	return render(request,'leaveform.html')



def formdis(request):
	data = []
	temp = {}
	if request.method == 'POST':

		# print '<><><',data
			# Available_leave = new_user.objects.get(Available_leave = Available_leave)
		# new_user_obj= new_user.objects.get(username = str(request.user))	
		
		datadump = user_leave.objects.all()
		# print datadump
		for i in datadump:
		   data.append({'user':i.user,'leave_type':i.leave_type,'From_date':i.From_date,'To_date':i.To_date,'Timeoff':i.Timeoff,'WDay_apply':i.WDay_apply,'Remarks':i.Remarks, 'id':i.id, 'available_leave': new_user.objects.get(username = i.user).Available_leave})
		print data
		return HttpResponse(content=json.dumps({'data': data}),content_type='Application/json')
	return render(request,'formdisplay.html')



def statusform(request):
	data=[]
	temp={}
	if request.method == 'POST':
		post, data, req_field = request.POST,{}, ['User','LeaveID','From_date','To_date','Status','Leave_type']
		for i in req_field:
			data[i] = post['leave[%s]'%i];
		print 'inside statusform'
		user_leav_obj = user_leave.objects.get(user=data['User'])
		print ' >>>>>>>>>>>>>>>>>'
		new_user_obj= new_user.objects.get(username=data['User'])
		mail = new_user_obj.mail
		print mail		
		da= user_leav_obj.WDay_apply
		al=new_user_obj.Available_leave
		remaining = al - da
		print remaining
		if remaining <= 0:
			print 'you not eligible to take further leave'
		else:
			print remaining
		print 'a'
		print 'inside statusform'
        new_user_obj.Available_leave = remaining
        new_user_obj.save()
        Leave_status.objects.create(
                                user=data['User'],
                                LeaveID=data['LeaveID'],
                                From_date=data['From_date'],
                                To_date=data['To_date'],
                                Status = data['Status'],
                                leave_type = data['Leave_type'],
                            )
		
        dump ='saved'
        send_mail_from_approver(data['From_date'],data['To_date'],data['Status'],mail);
	return render(request,'statusform.html')



def formdisplay(request):
	return render(request,'formdisplay.html')



def state(request):
	data =[]
	temp = {}
	if request.method == 'POST': 
		post = request.POST
		datadump = Leave_status.objects.all()
		for i in datadump:
		   data.append({'user':i.user,'leave_type':i.leave_type,'From_date':i.From_date,'To_date':i.To_date,'Status':i.Status})
		return HttpResponse(content=json.dumps({'data': data}),content_type='Application/json')
	return render(request,'statusform.html')



def send_message_to_user(user,leavetype,From_date,To_date,Timeoff,WDay_apply,Remarks):
	print 'data'
	print user
	print Remarks
	subject, from_email, to = 'Leave Apply', 'testeb@equityboss.com', 'mdyasin1992@gmail.com'
	text_content = 'this is text'	
	print text_content
	html_content=render_to_string('dddetails.html',{'user':user,'leavetype':leavetype,'From_date':From_date,'To_date':To_date,'Timeoff':Timeoff,'remark':Remarks,'WDay_apply':WDay_apply,})
	print 'in'
	msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
	print 'in1'
	msg.attach_alternative(html_content, "text/html")
	print 'in2'
	msg.send()
	print 'in3'



def send_mail_from_approver(From_date,To_date,Status,mail):
    print 'dat'
    print mail
    subject, from_email,to ='Leave Status', 'testeb@equityboss.com', mail
    text_content = 'this is text'
    print text_content
    html_content=render_to_string('approvermail.html',{'From_date':From_date,'To_date':To_date,'Status':Status,})
    print 'in'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    print 'in1'
    msg.attach_alternative(html_content, "text/html")
    print 'in2'
    msg.send()
    print 'in3'

	