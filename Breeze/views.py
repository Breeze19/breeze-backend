from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
import json
from .models import *
from .forms import *
from django.http import HttpResponseRedirect
from django.template import loader
import os
import random, string

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
    events = Events.objects.filter(category='sports')
    data_dict = {}
    for i in range(0,len(events)):
        fee = transform(events[i].fee)
        if(events[i].fee_snu != -1):
            fee = "Outside Participants: " + str(fee) + " | SNU Participants: " + transform(events[i].fee_snu)
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
    name = ""
    if(request.user.id is not None):
        name = request.user.profile.name
    context = {"js_data": js_data,"name": name}
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
    
def accomodation_brochure(request):
    return render(request,'accomodation.html')

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
         print(request.POST)
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
        }
        )
        if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
             User.objects.create_user(username, email, password)
             x = User.objects.last()
             Profile_obj = Profile.objects.create(user=x, name=name, contact=contact,college=college)
             user = authenticate(username=username, password=password)
             login(request, user)
             try:
                 send_mail(subject, message, "Breeze'19 "+from_email, to_list, fail_silently=False, html_message=html_message)
             except Exception as e:
                 print("error")
             return JsonResponse({
              "message": "success"
             })
        else:
            return JsonResponse({
            "message": "#userExists"
            })
    else:
        return JsonResponse({
        "message": "#invalidSignup"
        })         

def event_register2(request):
    if request.method == 'POST' and request.user.id is not None:
        e = int(request.POST['event'])
        event = Events.objects.get(id=e)
        print(event.name)
        uid = 'EV19{:02}{:04}'.format(event.id, request.user.id)
        try:
            print(event.fee_type)
            payable = 0
            if event.fee_type == 'team':
                payable = event.fee 
                if(event.name == 'Aagaaz'):
                    if int(request.POST['nop']) > 20:
                        payable = event.fee + (100 * (int(request.POST['nop']) - 20))
            elif event.fee_type == 'head':
                payable = event.fee * int(request.POST['nop'])
            payable1 = transform(payable)
            print(payable1)
        except Exception as exception:
            print(exception)
        if event.fee == 0:
            transaction_status = 'p'
        else:
            transaction_status = 'u'
        register = Registration(eventId=event, userId=request.user,
                                college=request.user.profile.college, registration_id=uid,transaction_status=transaction_status)       
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
        subject = "Event Registration Successful | Breeze'18"
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

def forgotmail(request):
    print(request.POST['email'], "\n\n")
    if request.method == "POST" :
        form=ForgotPassMailForm(request.POST)
        print(form)
        if form.is_valid():    
            print("Form Validation Successful")
            subject = "Reset Password | Breeze'18"
            message = "You can change your password here:-  "
            from_email = settings.DEFAULT_FROM_EMAIL
            print(request.POST['email'])
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
            print(os.getcwd())
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
                print(user)
                user = user.user
                user.set_password(password)
                user.save()
                ForgetPass.objects.filter(token=hashkey).delete()
                print("Password Changed Successfully")
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

#user profile and purchases
def dashboard(request):
        if request.user.id is not None:
            profile = Registration.objects.filter(userId=request.user)
            accreg = AccomRegistration.objects.filter(userId=request.user)
            context = {'profile':profile, 'accreg':accreg}
            return render(request,'dashboard.html',context=context)
        else:
            return HttpResponseRedirect('/#authreq2')

def accomodation(request):
    return render(request, 'help/accomodation.html')

def transport(request):
    return render(request, 'help/transport.html')

def pronights(request):
    return render(request, 'events/pronights.html')

def event_register(request):
    if request.method == 'POST' and request.user.id is not None:
        event = Events.objects.get(id=request.POST['event_id'])
        profile = request.user
        context = {
        'user': profile,
        'event' : event
        }
        return render(request, 'events/event_register.html',context=context)
    else:
        return HttpResponseRedirect('/#authrequired')

def accom_register(request):
    if request.user.id is not None:
        packages = AccPackage.objects.all()
        print(packages)
        context = {
            'packages' : packages
        }
        return render(request, 'help/accom_register.html', context=context)
    else:
        return HttpResponseRedirect('/#authrequired')

def accom_register2(request):
    next = ''
    if request.GET:
        next = request.GET['next']
        #print("I am Here 2")

    if request.method == 'POST' and request.user.id is not None:
        #print("I am Here")
        n = int(request.POST['number'])
        p = int(request.POST['package'])
        days = int(request.POST['days'])
        college = request.POST['college']
        #print(college)
        package = AccPackage.objects.get(id=p)
        if p == 2 or p == 4:
            payable = package.fee*n
        
        else:
            payable = package.fee*n*days
        uid = 'AC{:04}{:04}'.format(request.user.id, random.randint(1,9999))
        #print(uid)
        #id = ''.join(random.choice(string.ascii_uppercase) for _ in range(8))
        register = AccomRegistration(packageId=package, userId=request.user,
                                college=college, registration_id=uid, days=days, payable=payable, number=n)
        #print("I m here")
        try:
            register.save()
        except:
            return HttpResponseRedirect(next)

        subject = "Accommodation Registration Successful | Breeze'18"
        message = "Accommodation Registration Successful."
        from_email = settings.EMAIL_HOST_USER
        to_list = [request.user.email]
        html_message = loader.render_to_string(
            os.getcwd() + '/Breeze/templates/mails/AccomodationRegistration.html',
            {
                'name': request.user.profile.name,
                'email': request.user.email,
                'reg_id': uid,
                'package_name': package.name,
                'payable': payable,
                'number': n,
                'days': days,
                # 'user_name': username,
                # 'subject': 'Thank you for registering with us '+username+' \n You will now be recieving Notifications for howabouts at SNU in an all new Way. Goodbye to the spam mails. \n Thanks for registering. Have a nice day!!',
                # 'linkTosite': 'www.google.com',
            }
        )

        try:
            send_mail(subject, message, "Breeze'18 " + from_email,
                      to_list, fail_silently=False, html_message=html_message)
        except Exception as e:
            print("Mail not sent")
            print(e.message, e.args)

        return HttpResponseRedirect('/me/#accsuccess')
    else:
        return HttpResponseRedirect('/')
#
# def login_view(request):
#    redirect_to = request.REQUEST.get('next', '')
#    if request.method=='POST':
#       #create login form...
#       if valid login credentials have been entered:
#          return HttpResponseRedirect(redirect_to)
#    #...
#    return render_to_response('login.html', locals())
