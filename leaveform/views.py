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

@login_required
def signup(request):
    return render(request,'signup.html')

@login_required
def createaccount(request):
    if request.method == 'POST':
        post, data, req_field = request.POST, {}, ['username' ,'password','gender','dob','mail','mob','available_leave']
        for i in req_field:
            data[i] = post['all[%s]'%i]   
        if new_user.objects.filter(username = data['username']):
            dump = "registered"
        else:
            auth = User.objects.create_user(data['username'],'',data['password'])
            new_user.objects.create(
                                        available_leave=data['available_leave'],
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

        if user is not None:
            if user.is_active:
                login(request, user)
                if user.is_staff:
                    dump = "approverlogin"
                    return HttpResponse(content=json.dumps(dump),content_type='Application/json')
                dump = "userlogin"
                return HttpResponse(content=json.dumps(dump),content_type='Application/json')

            else:
                dump = "authentication failed"
                return HttpResponse(content=json.dumps(dump),content_type='Application/json')
        else:
            dump = "passwordauthenticationfailed"
            return HttpResponse(content=json.dumps(dump),content_type='Application/json')     
        return render(request,'login.html')
    if request.method == 'GET':     
      if request.user.is_anonymous():
        return render(request,'login.html')
      elif request.user.is_active:
        if request.user.is_staff:
          return HttpResponseRedirect('/formdisplay/')
        else:
          return HttpResponseRedirect('/home/')
    
@login_required
def home(request):
    loguser = request.user
    datadump=new_user.objects.get(auth = loguser)
    remaining_leave = datadump.available_leave
    return render(request, 'home.html',{'data':remaining_leave,'user':loguser})


def logout_view(request):
    logout(request)
    return render(request,'login.html')


@login_required
def leaveform(request):
    data =[]
    dat=str(request.user)
    if request.method == 'POST':
        post, data, req_field = request.POST, {}, ['leavetype' ,'From_date','To_date','Timeoff','WDapply','remark']
        for i in req_field:
            data[i] = post['all[%s]'%i]
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
        dump ='saved'
        send_message_to_user(currentuser,data['leavetype'],data['From_date'],data['To_date'],data['Timeoff'],data['WDapply'],data['remark']); #dat, data['Timeoff'],data['remark'])
        return HttpResponse(content=json.dumps(dump),content_type='Application/json')
    return render(request,'leaveform.html')


@login_required
def formdis(request):
    data = []
    data1 = []
    temp = {}
    if request.method == 'POST':

            # Available_leave = new_user.objects.get(Available_leave = Available_leave)
        # new_user_obj= new_user.objects.get(username = str(request.user))    
        showstatus = Leave_status.objects.filter(Status = 'Approve')
        for j in showstatus:
            data1.append({'user':j.user,'LeaveID':j.LeaveID,'From_date':j.From_date,'To_date':j.To_date,'Status':j.Status,'leave_type':j.leave_type})
        datadump = user_leave.objects.all()
        for i in datadump:
           data.append({'user':i.user,'leave_type':i.leave_type,'From_date':i.From_date,'To_date':i.To_date,'Timeoff':i.Timeoff,'WDay_apply':i.WDay_apply,'Remarks':i.Remarks, 'id':i.id, 'available_leave': new_user.objects.get(username = i.user).available_leave})
        return HttpResponse(content=json.dumps({'data': data}),content_type='Application/json')
    return render(request,'formdisplay.html')


@login_required
def statusform(request):
    data=[]
    temp={}
    if request.method == 'POST':
        post, data, req_field = request.POST,{}, ['User','LeaveID','Choose','From_date','To_date','Status','Leave_type']
        for i in req_field:
            data[i] = post['leave[%s]'%i];

        if data['Choose'] == 'true':
            user_leav_obj = user_leave.objects.get(user=data['User'])
            print user_leav_obj
            new_user_obj= new_user.objects.get(username=data['User'])
            print new_user_obj
            mail = new_user_obj.mail            
            da= user_leav_obj.WDay_apply
            print da
            al=new_user_obj.available_leave
            print al
            ls = Leave_status.objects.filter(user=data['User'])
            print ls
            # if ls:
            #     ls = ls[0]
            #     ls.Status = data['Status']
            #     ls.save()  

            # if ls:
            if data['Status'] == 'Approve' :
                    remaining = (int(al) - int(da))
                    print remaining
                    status = 'Approve'
                    if remaining < 0:
                        dump = "error"
                        return HttpResponse(content=json.dumps(dump),content_type='Application/json')
                    else:
                        new_user_obj.available_leave = remaining
                        new_user_obj.save()
                        Leave_status.objects.create(
                                                user=data['User'],
                                                LeaveID=data['LeaveID'],
                                                From_date=data['From_date'],
                                                To_date=data['To_date'],
                                                Status = status,
                                                leave_type = data['Leave_type'],
                                            )
                        
                        dump ='saved'
                        send_mail_from_approver(data['From_date'],data['To_date'],status,mail);
                        user_obj = user_leave.objects.get(user=data['User'])
                        user_obj.delete()
                        return HttpResponse(content=json.dumps(dump),content_type='Application/json')

            elif data['Status'] == 'Pending' :
                    status = 'Pending'                
                    Leave_status.objects.create(
                                            user=data['User'],
                                            LeaveID=data['LeaveID'],
                                            From_date=data['From_date'],
                                            To_date=data['To_date'],
                                            Status = status,
                                            leave_type = data['Leave_type'],
                                        )
                    
                    dump ='saved'
                    send_mail_from_approver(data['From_date'],data['To_date'],status,mail);
                    return HttpResponse(content=json.dumps(dump),content_type='Application/json')


            elif data['Status'] == 'Reject' :
                    status = 'Reject'                
                    Leave_status.objects.create(
                                            user=data['User'],
                                            LeaveID=data['LeaveID'],
                                            From_date=data['From_date'],
                                            To_date=data['To_date'],
                                            Status = status,
                                            leave_type = data['Leave_type'],
                                        )
                    
                    dump ='saved'
                    send_mail_from_approver(data['From_date'],data['To_date'],status,mail);
                    user_obj = user_leave.objects.get(user=data['User'])
                    print user_obj
                    user_obj.delete()
                    return HttpResponse(content=json.dumps(dump),content_type='Application/json')
        elif data['Choose'] == 'false':
            dump = "nothing"
            return HttpResponse(content=json.dumps(dump),content_type='Application/json')

        elif data['Status'] == True:
            print 'amin'
                
    return render(request,'statusform.html')


@login_required
def formdisplay(request):
    return render(request,'formdisplay.html')


@login_required
def state(request):
    data = []
    curruser = request.user
    datadump = Leave_status.objects.filter(user = curruser)
    for i in datadump:
        data.append({'user':i.user,'leave_type':i.leave_type,'From_date':i.From_date,'To_date':i.To_date,'Status':i.Status})
    return HttpResponse(content=json.dumps({'data': data}),content_type='Application/json')
    # return render(request,'home.html')



def send_message_to_user(user,leavetype,From_date,To_date,Timeoff,WDay_apply,Remarks):
    subject, from_email, to = 'Leave Apply', 'testeb@equityboss.com', 'sadam@ithoughtz.com'
    text_content = 'this is text'    
    html_content=render_to_string('dddetails.html',{'user':user,'leavetype':leavetype,'From_date':From_date,'To_date':To_date,'Timeoff':Timeoff,'remark':Remarks,'WDay_apply':WDay_apply,})
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()



def send_mail_from_approver(From_date,To_date,Status,mail):
    subject, from_email,to ='Leave Status', 'testeb@equityboss.com', mail
    text_content = 'this is text'
    html_content=render_to_string('approvermail.html',{'From_date':From_date,'To_date':To_date,'Status':Status,})
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def forgotpassword(request):
    return render(request,'forgotpassword.html')

