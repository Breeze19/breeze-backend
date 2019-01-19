from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
import json
from .models import *
from .forms import *
from django.http import HttpResponseRedirect,HttpResponse
from django.template import loader
import os
import random, string
from .config import *
import csv

def get_reg_csv(request,key):
    try:
        if(key == API_KEY):
            registerations = Registration.objects.all()
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="registrations.csv"'
            writer = csv.writer(response)
            writer.writerow(['','Registration id','Transaction status','Name','NOP','Payable','College','Category','Email ID','Phone','Event Name'])
            for i in range(0,len(registerations)):
                row = []
                row.append(i)
                row.append(registerations[i].registration_id)
                if(registerations[i].transaction_status == 'p'):
                    row.append('paid')
                elif(registerations[i].transaction_status == 'u'):
                    row.append('unpaid')
                else:
                    row.append('disperancy')
                row.append(registerations[i].userId.profile.name)
                row.append(registerations[i].nop)
                row.append(registerations[i].payable)
                row.append(registerations[i].college)
                if(registerations[i].eventId.category == 'c'):
                    row.append('cultural')
                elif(registerations[i].eventId.category == 's'):
                    row.append('sports')
                else:
                    row.append('technical')
                row.append(registerations[i].userId.email)
                row.append(registerations[i].userId.profile.contact)
                row.append(registerations[i].eventId.name)
                writer.writerow(row)
            return response
        else:
            return HttpResponseRedirect('/')
    except Exception as exception:
        print(exception)

def view_reg(request,key):
    try:
        if(key == API_KEY):
            registerations = Registration.objects.all()
            context = {"registrations": registerations}
            return render(request,'table.html',context=context)
        else:
            return HttpResponseRedirect('/')
    except Exception as exception:
        print(exception)

def view_reg_club(request,key,clubname):
    try:
        if(key == API_KEY):
            registerations = Registration.objects.all()
            name = clubname
            if name.lower == 'wordsink':
                name = 'words.ink'
            elif name.lower == 'designclub':
                name = 'design club'
            elif name.lower == 'gogreen':
                name = 'go green'
            elif name.lower == 'naturesentinel':
                name = 'naturesentinel'
            elif name.lower == 'treasurehunt':
                name = 'treasure hunt'
            regis_club = []
            for i in range(0,len(registerations)):
                if(registerations[i].eventId.parentClub.lower() == name.lower()):
                    regis_club.append(registerations[i])
            context = {"registrations": regis_club}
            return render(request,'table.html',context=context)
        else:
            return HttpResponseRedirect('/')
    except Exception as exception:
        print(exception)

def home(request):
    return render(request, 'index.html')
    
def nineteen(request):
    return redirect('/')

def get_events(request):
    if(request.user.id is not None):
        name = request.user.profile.name
        context = {"name": name}
        return render(request, 'events.html',context=context)
    return render(request, 'events.html')
    
def technical(request):
    if(request.user.id is not None):
        name = request.user.profile.name
        context = {"name": name}
        return render(request, 'eventstechcat.html',context=context)
    return render(request, 'eventstechcat.html')

def cultural(request):
    if(request.user.id is not None):
        name = request.user.profile.name
        context = {"name": name}
        return render(request, 'eventsculcat.html',context=context)
    return render(request, 'eventsculcat.html')

def sports(request):
    events = Events.objects.filter(category='s')
    data_dict = {}
    for i in range(0,len(events)):
        fee = transform(events[i].fee)
        if(events[i].fee_snu != -1):
            fee = "Outside Participants: " + str(fee) + " | SNU Participants: " + transform(events[i].fee_snu)
        data_dict[events[i].id] = {
        "name": events[i].name,
        "rules": events[i].rules,
        "date": str(events[i].date),
        "prize": events[i].prizes,
        "fee": fee + " Per head",
        "contact_name": events[i].contact_market
        }
    js_data = json.dumps(data_dict)
    name = ""
    if(request.user.id is not None):
        name = request.user.profile.name
    context = {"js_data": js_data,"name": name,"events": events}
    return render(request, 'eventssportscat.html',context=context)

def sportstkk(request):
    if(request.user.id is not None):
        name = request.user.profile.name
        context = {"name": name}
        return render(request, 'formtkk.html',context=context)
    return render(request,'formtkk.html')
    
def sportstkp(request):
    if(request.user.id is not None):
        name = request.user.profile.name
        context = {"name": name}
        return render(request, 'formtkp.html',context=context)
    return render(request,'formtkp.html')
    
def gallery(request):
    if(request.user.id is not None):
        name = request.user.profile.name
        context = {"name": name}
        return render(request, 'gallery.html',context=context)
    return render(request,'gallery.html')
    
def sponsors(request):
    if(request.user.id is not None):
        name = request.user.profile.name
        context = {"name": name}
        return render(request, 'sponsors.html',context=context)
    return render(request,'sponsors.html')
    
def forgotpassmail(request):
    if(request.user.id is not None):
        name = request.user.profile.name
        context = {"name": name}
        return render(request, 'Resetpassemail.html',context=context)
    return render(request,'Resetpassemail.html')
    
def team(request):
    if(request.user.id is not None):
        name = request.user.profile.name
        context = {"name": name}
        return render(request, 'team.html',context=context)
    return render(request,'team.html')

def dashboard(request):
    if request.user.id is not None:
        profile = Registration.objects.filter(userId=request.user)
        accreg = AccomRegistration.objects.filter(userId=request.user)
        context = {'profiles':profile,"accomodations": accreg}
        return render(request,'dashboard.html',context=context)

def accomodation_brochure(request):
    return render(request,'acc_brochure.html')

def accomodation(request):
    context = {"name": "","email": "","phno": "","college": ""}
    if(request.user.id is not None):
        context = {"name":request.user.profile.name,"email": request.user.email,"phno": request.user.profile.contact,"college": request.user.profile.college}
    return render(request,'accomodation.html',context=context)

def sports_handbook(request):
    return render(request,'sportshandbook.html')
    
def specificEventView(request,category,subcategory):
    name = ""
    if(request.user.id is not None):
        name = request.user.profile.name
    color = "#e25c7f"
    if category == "technical":
        color = "#fafafa"
    events = Events.objects.filter(category=category[0]).filter(subCategory=subcategory)
    data_dict = {}
    for i in range(0,len(events)):
        fee = transform(events[i].fee)
        if(events[i].fee_snu != -1):
            fee = "Outside Participants: " + fee + " | SNU Participants: " + transform(events[i].fee_snu)
        data_dict[events[i].id] = {
        "name": events[i].name,
        "description": events[i].description,
        "rules": events[i].rules,
        "date": str(events[i].date),
        "prize": transform(events[i].prize),
        "fee": fee,
        "contact_name": events[i].contact_market
        }
    js_data = json.dumps(data_dict)
    context  = {'events': events, 'subcategory': subcategory,"color": color,'category': category,"js_data": js_data,"name": name}
    return render(request, 'eventssubcat.html',context=context)

def transform(amount):
    t_amt = "Rs "
    try:
        amt = str(amount)
    except Exception as exception:
        print(exception)
    try:
        if amount == 0:
            return "No Registration Fee"
        if amount >= 100000:
            t_amt += amt[0:1] + "," + amt[1:3] + "," + amt[3:]
        elif amount >= 10000 and amount < 100000:
            t_amt += amt[0:2] + "," + amt[2:]
        elif amount >= 1000 and amount < 10000:
            t_amt += amt[0:1] + "," + amt[1:]
        elif amount >=1 and amount < 1000:
            t_amt += amt
        return t_amt[0:len(t_amt)-3]
    except Exception as exception:
        print(exception)

def transform1(amount):
    t_amt = "Rs "
    try:
        amt = str(amount)
    except Exception as exception:
        print(exception)
    try:
        if amount == 0:
            return "No Registration Fee"
        if amount >= 100000:
            t_amt += amt[0:1] + "," + amt[1:3] + "," + amt[3:]
        elif amount >= 10000 and amount < 100000:
            t_amt += amt[0:2] + "," + amt[2:]
        elif amount >= 1000 and amount < 10000:
            t_amt += amt[0:1] + "," + amt[1:]
        elif amount >=1 and amount < 1000:
            t_amt += amt
        return t_amt
    except Exception as exception:
        print(exception)

def signin(request):
    name = ""
    if(request.user.id is not None):
        name = request.user.profile.name
    try:
        val = request.GET['prev']
    except Exception as exception:
        val = ""    
    context = {'prev': val,"name": name}
    return render(request,'Signin.html',context=context)
    
def register(request):
    name = ""
    if(request.user.id is not None):
        name = request.user.profile.name
    try:
        val = requet.GET['prev']
    except Exception as exception:
        val = ""    
    context = {'prev': val,"name": name}
    return render(request,'Signup.html',context=context)

def login1(request):
    if request.method == 'POST':
         user = authenticate(username=request.POST['username'], password = request.POST['password'])
         if not user or not user.is_active:
                 return JsonResponse({
                 "message": '#invalidUser'
                 })
         try:
             login(request,user)
         except Exception as exception:
             return JsonResponse({
             "message": '#couldNotLogin'
             })
         return JsonResponse({
         "message": "success"
         })
    
def createaccount(request):
    if request.method == 'POST':
        name = request.POST['name']
        email =  request.POST['email']
        username = email
        password =request.POST['password']
        confirm = request.POST['confirmpass']
        contact = request.POST['contact']
        college = request.POST['college']
        subject = "Welcome to Breeze'19"
        message = "Welcome to Breeze 19 by SNU. "
        from_email = settings.DEFAULT_FROM_EMAIL
        to_list = [email]
        html_message = loader.render_to_string(
        os.getcwd()+'/Breeze/templates/signup_mail.html',
        {
         'name' : name,
         'username': email,
         'password': password
        }
        )
        try:
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
                x = User.objects.last()
                Profile_obj = Profile.objects.create(user=x, name=name, contact=contact,college=college)
                user = authenticate(username=username, password=password)
                login(request, user)
                try:
                    send_mail(subject, message, "Breeze'19 "+from_email, to_list, fail_silently=False, html_message=html_message)
                except Exception as exception:
                    print(exception)
                return JsonResponse({
                "message": "success"
                })
            else:
                return JsonResponse({
                "message": "#userExists"
                })
        except Exception as exception:
            print(exception)
            return JsonResponse({
            "message": "Try Again"
            })
    else:
        return JsonResponse({
        "message": "#invalidSignup"
        })         

def event_register2(request):
    if request.method == 'POST' and request.user.id is not None:
        e = int(request.POST['event'])
        event = Events.objects.get(id=e)
        uid = 'EV19{:02}{:04}'.format(event.id, request.user.id)
        payable = 0
        try:
            if event.fee_type == 'team':
                payable = event.fee 
                if event.fee_snu != -1:
                    if(str(request.user.email).endswith('snu.edu.in')):
                        payable = event.fee_snu
                if(event.name == 'Aagaaz'):
                    if int(request.POST['nop']) > 20:
                        payable = event.fee + (100 * (int(request.POST['nop']) - 20))
            elif event.fee_type == 'head':
                payable = event.fee * int(request.POST['nop'])
                if event.fee_snu != -1:
                    if(str(request.user.email).endswith('snu.edu.in')):
                        payable = event.fee_snu * int(request.POST['nop'])
        except Exception as exception:
            print(exception)
        if event.fee == 0:
            transaction_status = 'p'
        else:
            transaction_status = 'u'
        try:
            register = Registration(eventId=event, userId=request.user,
                                college=request.user.profile.college, registration_id=uid,transaction_status=transaction_status,
                                payable=payable,nop=int(request.POST['nop']))       
        except Exception as exception:
            return JsonResponse({
            "message": "Try again"
            })
            print(exception)
        try:
            register.save()
        except Exception as exception:
            print(exception)
            return JsonResponse({
            "message": "Error while recording registration. Please try again."
            })
        form_url = ""
        if(event.form_url != "null") :
            form_url = event.form_url
        subject = "Event Registration Successful | Breeze'19"
        message = "Event Registration Successful."
        from_email = settings.DEFAULT_FROM_EMAIL
        to_list = [request.user.email]
        if(form_url == "null"):
            html_message = loader.render_to_string(
                os.getcwd()+'/Breeze/templates/reg_mail.html',
                {
                    'name' : request.user.profile.name,
                    'email' : request.user.email,
                    'reg_id' : uid,
                    'event_name' : event.name,
                    'status': transaction_status,
                    'amount': transform(payable)
                }
            )  
        else:
            html_message = loader.render_to_string(
                os.getcwd()+'/Breeze/templates/reg_mail1.html',
                {
                    'name' : request.user.profile.name,
                    'email' : request.user.email,
                    'reg_id' : uid,
                    'event_name' : event.name,
                    'status': transaction_status,
                    'form_url': form_url,
                    'amount': transform(payable)
                }
            )        
        try:
            send_mail(subject, message, from_email, to_list, fail_silently=False, html_message=html_message)                
        except Exception as e:
            print("Mail not sent")
            print (e.message, e.args)

        return JsonResponse({
        "message": "success"
        })
    else:
        return JsonResponse({
        "message": "Please signin first."
        })

def accom_register(request):
    if request.method == 'POST':
        if request.user.id is not None:
            package = request.POST['package']
            days = int(request.POST['days'])
            food = request.POST['meal']
            if food == 'Without Meals':
                packageid = AccPackage.objects.get(name=package)   
            else:
                packageid = AccPackage.objects.get(name=package + " (" + food + ")")   
            fee = 0
            if(package == 'Per Day Package'):
                fee = days * 300
                if(food == 'With Meals'):
                    fee += days * 150
            else:
                if(food == 'With Meals'):
                    fee = 1250
                else:
                    fee = 800
            uid = 'AC{:04}{:04}'.format(request.user.id, random.randint(1,9999))
            register = AccomRegistration(packageId=packageid, userId=request.user,
                                college=request.user.profile.college, registration_id=uid, days=days, payable=fee)
            try:
                register.save()
            except:
                return JsonResponse({
                "message": "Already registered for accomodation"
                })
            subject = "Accomodation Registration Successful | Breeze'19"
            message = "Accomodation Registration Successful."
            from_email = settings.DEFAULT_FROM_EMAIL
            to_list = [request.user.email]
            try:
                html_message = loader.render_to_string(
                    os.getcwd()+'/Breeze/templates/accomodation_mail.html',
                    {
                        'name' : request.user.profile.name,
                        'reg_id' : uid,
                        'package' : packageid.name,
                        'amount': transform1(fee)
                        }
                        )  
                send_mail(subject, message, from_email, to_list, fail_silently=False, html_message=html_message)                
                        
            except Exception as exception:
                print(exception)
            return JsonResponse({
            "message": 'success'
            })
        else:
            return JsonResponse({
            "message": "Please signin first"
            })

def forgotmail(request):
    if request.method == "POST" :
        form=ForgotPassMailForm(request.POST)
        if form.is_valid():    
            subject = "Reset Password | Breeze'19"
            message = "You can change your password here:-  "
            from_email = settings.DEFAULT_FROM_EMAIL
            to_list = [request.POST['email']]
            url_hash= "".join(random.choice(string.ascii_letters + string.digits) for _ in range(64))
            try:
                user=User.objects.filter(username=request.POST['email'].strip())
                if(user.exists()):
                    ForgetPass.objects.create(token=url_hash,user=user[0])                
            except Exception as exception:
                print(exception)
                return JsonResponse({
                "message": "Password reset error"
                })
            html_message = loader.render_to_string(
                os.getcwd()+'/Breeze/templates/forgot_pass.html',
                    {
                    'link' : 'https://breeze19.appspot.com/forgotPassword/' + url_hash,
                    'subject': 'Password reset email'
                }
            )
            try:
                send_mail(subject, message, from_email, to_list, fail_silently=False, html_message=html_message)                
            except Exception as e:
                print("Mail not sent")
                print (e.message, e.args)
            return JsonResponse({
            "message": "success"
            })
        else:
            raise forms.ValidationError("Form can not be Validated.")

def forgot(request,hashkey):
    if request.method == "POST":
        password = request.POST['password']
        confirm = request.POST['repassword']
        if(password==confirm):
            try:
                user = ForgetPass.objects.filter(token=hashkey)[0]
                user = user.user
                user.set_password(password)
                user.save()
                ForgetPass.objects.filter(token=hashkey).delete()
                return JsonResponse({
                "message": "success"
                })
            except:
                raise forms.ValidationError("Unable to Change Password")
        else:
            return JsonResponse({
            "message": "You had one job; Type the same password"
            })
    else:
        if(len(hashkey)!=64):
            return HttpResponseRedirect('/')
        forget_pass_object = ForgetPass.objects.filter(token=hashkey)
        if not forget_pass_object:
            return HttpResponseRedirect('/')
        return render(request, "Resetpass.html", {"hashkey" : hashkey})
    
def clubdashboard(request):
    if request.method == 'GET':
        events = Events.objects.all()
        registrations = Registration.objects.all()
        context = {
            'events' : events,
            'registrations': registrations
        }
        return render(request, 'clubdashboard.html', context=context)

    if request.method == 'POST':
        id = request.POST['event']
        name = request.POST['event_name']
        registrations = Registration.objects.filter(eventId=id)
        events = Events.objects.all()
        context = {
            'registrations' : registrations,
            'events' : events,
            'event_name' : name
        }
        return render(request, 'clubdashboard.html', context=context)

def updateremarks(request):
    if request.method == 'POST' and request.user.username == 'priyanshrastogi' or request.user.username == 'breeze.events@snu.edu.in':
        rid = request.POST['regId']
        remarks = request.POST['remarks']

        reg = Registration.objects.get(pk=rid)
        reg.remarks = remarks
        reg.save()
        return HttpResponseRedirect('/clubdashboard')

def partners(request):
    return render(request, 'help/partners.html')

def transport(request):
    return render(request, 'help/transport.html')

def pronights(request):
    return render(request, 'events/pronights.html')