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
import pyrebase
    
def home(request):
    return render(request, 'index.html')
    
def nineteen(request):
    return redirect('/')

def get_events(request):
    return render(request, 'events.html')
    
def technical(request):
    return render(request, 'eventstechcat.html')

def cultural(request):
    return render(request, 'eventsculcat.html')
    
def id(request):
    return render(request,'gen_id.html')        
        
def gallery(request):
    return render(request,'gallery.html')
    
def sponsors(request):
    return render(request,'sponsors.html')
    
def forgotpassmail(request):
    return render(request,'Resetpassemail.html')
    
def team(request):
    return render(request,'team.html')

def accomodation_brochure(request):
    return render(request,'acc_brochure.html')
    
def transport(request):
    return render(request,'transport.html')

def sports_handbook(request):
    return render(request,'sportshandbook.html')

def accomodation(request):
    context = {"name": "","email": "","phno": "","college": ""}
    if(request.user.id is not None):
        context = {"name":request.user.profile.name,"email": request.user.email,"phno": request.user.profile.contact,"college": request.user.profile.college}
    return render(request,'accomodation.html',context=context)

def dashboard(request):
    if request.user.id is not None:
        profile = Registration.objects.filter(userId=request.user)
        accreg = AccomRegistration.objects.filter(userId=request.user)
        context = {'profiles':profile,"accomodations": accreg}
        return render(request,'dashboard.html',context=context)
    
def signin(request):
    try:
        val = request.GET['prev']
    except Exception as exception:
        val = ""    
    context = {'prev': val}
    return render(request,'Signin.html',context=context)
    
def register(request):
    try:
        val = requet.GET['prev']
    except Exception as exception:
        val = ""    
    context = {'prev': val}
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
         
def specificEventView(request,category,subcategory):
    color = "#e25c7f"
    if category == "technical":
        color = "#fafafa"
    events = Events.objects.filter(category=category[0]).filter(subCategory=subcategory)
    data_dict = {}
    for i in range(0,len(events)):
        include = 1
        fee = transform(events[i].fee)
        if len(str(events[i].prizes).strip()) > 1 or str(events[i].prize) == 'null':
            prize = events[i].prizes
        else:
            prize = transform(events[i].prize)
        if(events[i].fee_snu != -1):
            fee = "Outside Participants: " + fee + " | SNU Participants: " + transform(events[i].fee_snu)
        data_dict[events[i].id] = {
        "name": events[i].name,
        "description": events[i].description,
        "rules": events[i].rules,
        "date": str(events[i].date),
        "prize": prize,
        "fee": fee,
        "contact_name": events[i].contact_market,
        "include": include
        }
    js_data = json.dumps(data_dict)
    context  = {'events': events, 'subcategory': subcategory,"color": color,'category': category,"js_data": js_data}
    return render(request, 'eventssubcat.html',context=context)
         
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
    context = {"js_data": js_data,"events": events}
    return render(request, 'eventssportscat.html',context=context)         
         
def gen_id(request):
    try:
        if request.method == 'POST':
            name = request.POST['name']
            college = request.POST['college']
            rollno = request.POST['rollno']
            email = request.POST['email']
            yos = request.POST['yos']
            number = request.POST['phno'],
            participant = request.POST["participant"]
            subject = "Breeze19 ID"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_list = [email]
            html_message = loader.render_to_string(
            os.getcwd() + '/Breeze/templates/id_mail.html',
            {
            "name": name,
            "college": college,
            "rollno": rollno,
            "yos": yos,
            "email": email,
            'participant': participant,
            'phno': number
            })
            try:
                send_mail(subject, subject, "Breeze'19 "+from_email, to_list, fail_silently=False, html_message=html_message)
            except Exception as exception:
                print(exception)
                return JsonResponse({
                "message": "ID creation failed. Try again."
                })
            return JsonResponse({
            "message": "Breeze ID has been emailed to you.\nPlease show the same along with your College ID to the Security Team to gain entry"
            })    
    except Exception as exception:
        priint(exception)
            
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
                try:
                    Profile_obj.save()
                except Exception as exp:
                    print(exp)
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
            usr_profile = Profile.objects.filter(user=request.user)
            if len(usr_profile) > 0:
                register = Registration(eventId=event, userId=request.user,
                                    college=usr_profile.last().college, registration_id=uid,transaction_status=transaction_status,
                                    payable=payable,nop=int(request.POST['nop']))               
            else:
                return JsonResponse({
                "message": "Error"
                })
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
        if(event.form_url == "null"):
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

def pronights(request):
    return render(request, 'events/pronights.html')

# Util functions

def ga_tracking_id(request):
    return {'ga_tracking_id': GA_TRACKING_ID}

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
    
# Admin routes

def get_events_data(request,category,apikey):
    try:
        if apikey == API_KEY:
            events = Events.objects.filter(category=category[0])
            json_rep = {}
            for i in range(0,len(events)):
                json_rep[events[i].id] = {
                "name": events[i].name,
                "description": events[i].description,
                "date": str(events[i].date),
                "venue": events[i].venue,
                "contact_name": events[i].contact_market
                }
            return JsonResponse({
            "status": 205,
            "message": "success",
            "data": json.dumps(json_rep)
            })
        else:
            return JsonResponse({
            "status": 303,
            "message": "Not authorized"
            })
    except Exception as exception:
        print(exception)
        return JsonResponse({
        "status": 500,
        "message": "Internal server error"
        })

def push_events_to_firebase(request,apikey):
    try:
        if apikey == API_KEY:
            events = Events.objects.all()
            json_rep = {}
            for i in range(0,len(events)):
                category = ''
                if(events[i].category == 'c'):
                    category = 'cultural'
                elif(events[i].category == 's'):
                    category = 'sports'
                else:
                    category = 'technical'
                json_rep[events[i].id] = {
                "eventsName": events[i].name,
                "eventsDetails": events[i].description,
                "eventDate": str(events[i].date),
                "eventVenue": events[i].venue,
                "eventContact": events[i].contact_market,
                "eventCategory": category
                }
            firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
            db = firebase.database()
            db.child("data").child("events").set(json_rep)
            return JsonResponse({
            "status": 200,
            "message": "success"
            })
        else:
            return JsonResponse({
            "status": 303,
            "message": "Not authorized"
            })
    except Exception as exception:
        print(exception)
        return JsonResponse({
        "status": 500,
        "message": "Internal server error"
        })

def get_acc_reg_csv(request,key):
    try:
        if(key == KEY):
            acc_registrations = AccomRegistration.objects.all()
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="acc_registrations.csv"'
            writer = csv.writer(response)
            writer.writerow(['','Registration ID','Package Name','Participant Name','Days','Payable','College','Transaction Status'])
            for i in range(0,len(acc_registrations)):
                row = []
                row.append(i)
                row.append(acc_registrations[i].registration_id)
                row.append(acc_registrations[i].packageId.name)
                row.append(acc_registrations[i].userId.profile.name)
                row.append(acc_registrations[i].days)
                row.append(acc_registrations[i].payable)
                row.append(acc_registrations[i].college)
                if(acc_registrations[i].transaction_status == 'u'):
                    row.append('unpaid')
                else:
                    row.append('paid')
                writer.writerow(row)
            return response
        else:
            return JsonResponse({
            "status": 303,
            "message": "Forbidden"
            })
    except Exception as exception:
        print(exception)
        return JsonResponse({
        "status": 500,
        "message": "Internal Server Error"
        })

def get_profiles_csv(request,key):
    try:
        if(key == KEY):
            profile_data = Profile.objects.all()
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="profiles.csv"'
            writer = csv.writer(response)
            writer.writerow(['','Name','Email','Contact','College'])
            for i in range(0,len(profile_data)):
                row = []
                row.append(i)
                row.append(profile_data[i].name)
                row.append(profile_data[i].user.email)
                row.append(profile_data[i].contact)
                row.append(profile_data[i].college)
                writer.writerow(row)
            return response
        else:
            return JsonResponse({
            "status": 303,
            "message": "Forbidden"
            })
    except Exception as exception:
        print(exception)
        return Jsonresponse({
        "status": 500,
        "message": "Internal Server Error"
        })
    
def get_reg_csv(request,key):
    try:
        if(key == KEY):
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
            return JsonResponse({
            "status": 303,
            "message": "Forbidden"
            })
    except Exception as exception:
        print(exception)
        return JsonResponse({
        "status": 500,
        "message": "Internal Server Error"
        })

def view_reg(request,key):
    try:
        if(key == KEY):
            registerations = Registration.objects.all()
            context = {"registrations": registerations}
            return render(request,'table.html',context=context)
        else:
            return HttpResponseRedirect('/')
    except Exception as exception:
        print(exception)

def view_reg_club(request,key,clubname):
    try:
        if(key == KEY):
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