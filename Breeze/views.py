from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from .models import *
from .forms import *
from django.http import HttpResponseRedirect
from django.template import loader
import os
import random, string

# Create your views here.

def home(request):
    return render(request, 'index.html')

def get_events(request):
    return render(request, 'events.html')
    
def technical(request):
    return render(request, 'eventstechcat.html')

def cultural(request):
    return render(request, 'eventsculcat.html')

def sports(request):
    return render(request, 'events/sports.html')
    
def specificEventView(request,category,subcategory):
    events = Event.objects.filter(category=category[0]).filter(subCategory=subcategory)
    context  = {'events': events, 'subcategory': subcategory}
    return render(request, 'eventssubcat.html', context=context)

def clubdashboard(request):
    if request.method == 'GET':
        events = Event.objects.all()
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
        events = Event.objects.all()
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
def profile(request):
        if request.user.id is not None:
            profile = Registration.objects.filter(userId=request.user)
            accreg = AccomRegistration.objects.filter(userId=request.user)
            context = {'profile':profile, 'accreg':accreg}
            return render(request,'user.html',context=context)
        else:
            return HttpResponseRedirect('/#authreq2')

def accomodation(request):
    return render(request, 'help/accomodation.html')

def transport(request):
    return render(request, 'help/transport.html')

def pronights(request):
    return render(request, 'events/pronights.html')

def team(request):
    return render(request, 'help/team.html')

def eighteen(request):
    return redirect('/')

def pdf_redirect(request):
    return redirect('/static/Breeze_2018_Sponsorship_Brochure.pdf')

def event_register(request):
    if request.method == 'POST' and request.user.id is not None:
        event = Event.objects.get(id=request.POST['event_id'])
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

def event_register2(request):
    next = ''
    if request.GET:
        next = request.GET['next']

    if request.method == 'POST' and request.user.id is not None:
        e = int(request.POST['event'])
        college = request.POST['college']
        print(college)
        event = Event.objects.get(id=e)
        uid = 'EV18{:02}{:04}'.format(event.id, request.user.id)
        if event.fee_type == 'head':
            number = int(request.POST['number'])
            payable = event.fee*number

        else:
            payable = event.fee
            number = int(request.POST['number'])

        if event.fee == 0:
            transaction_status = 'p'

        else:
            transaction_status = 'u'

        register = Registration(eventId=event, userId=request.user,
                                college=college, registration_id=uid, payable=payable, number_of_participants=number, transaction_status=transaction_status)
       
        try:
            register.save()
        except:
            return HttpResponseRedirect(next)
        
        form_url = ""
        if(event.form_url != "null") :
            arr = event.form_url.split("EV12345678")
            form_url = arr[0]+uid+arr[1]

        subject = "Event Registration Successful | Breeze'18"
        message = "Event Registration Successful."
        from_email = settings.EMAIL_HOST_USER
        to_list = [request.user.email]
        html_message = loader.render_to_string(
            os.getcwd()+'/Breeze/templates/mails/EventRegistrationMail.html',
            {
                'name' : request.user.profile.name,
                'email' : request.user.email,
                'reg_id' : uid,
                'event_name' : event.name,
                'payable': payable,
                'status': transaction_status,
                'form_url': form_url,
                'form_text': event.form_text
                # 'user_name': username,
                # 'subject': 'Thank you for registering with us '+username+' \n You will now be recieving Notifications for howabouts at SNU in an all new Way. Goodbye to the spam mails. \n Thanks for registering. Have a nice day!!',
                # 'linkTosite': 'www.google.com',
            }
        )
        
        try:
            send_mail(subject, message, "Breeze'18 "+from_email, to_list, fail_silently=False, html_message=html_message)                
        except Exception as e:
            print("Mail not sent")
            print (e.message, e.args)

        return HttpResponseRedirect('/me/#success')
    
    else:
        return HttpResponseRedirect('/')

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

def login1(request):
    next = ""
    if request.GET:
        next = request.GET['next']

    if request.method=="POST":
        user = authenticate(username=request.POST['username'], password = request.POST['password'])
        if not user or not user.is_active:
            return HttpResponseRedirect('/#invalidlogin')
        
        #print("user===",user)
        #print(user.username)
        print(request)
        try:
            login(request,user)
        except Exception as e:
            raise forms.ValidationError("Could Not Login")
            # print (e.message, e.args)
        #print(request.user.username)
        return HttpResponseRedirect(next)

def register(request):
    # redirect_to = request.REQUEST.get('next')
    # print(redirect_to)
    next = ""

    if request.GET:
        next = request.GET['next']

    if request.method=="POST":
        name = request.POST['name']
        email =  request.POST['email']
        username = email
        password =request.POST['password']
        confirm = request.POST['confirmpass']
        contact = request.POST['contact']
        if(password==confirm):
            subject = "Welcome to Breeze'19"
            message = "Welcome to Breeze 19 by SNU. "
            from_email = settings.EMAIL_HOST_USER
            to_list = [email]
            html_message = loader.render_to_string(
                os.getcwd()+'/Breeze/templates/mails/SigningupMail.html',
                {
                    'name' : name,
                    'email' : email
                    # 'user_name': username,
                    # 'subject': 'Thank you for registering with us '+username+' \n You will now be recieving Notifications for howabouts at SNU in an all new Way. Goodbye to the spam mails. \n Thanks for registering. Have a nice day!!',
                    # 'linkTosite': 'www.google.com',
                }
            )
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
                x = User.objects.last()
                Profile_obj = Profile.objects.create(user=x, name=name, contact=contact)
                user = authenticate(username=username, password=password)
                login(request, user)
                #print("User created Successfully")
                try:
                    send_mail(subject, message, "Breeze'19 "+from_email, to_list, fail_silently=False, html_message=html_message)
                except Exception as e:
                    print("Mail not sent")
                    print (e.message, e.args)
                return HttpResponseRedirect(next)
            else:
                #raise forms.ValidationError('Looks like a username with that email or password already exists')
                return HttpResponseRedirect("/#userexists")
        else:
            #raise forms.ValidationError('Password not confirmed.')
            return HttpResponseRedirect("/#invalidsignup")

#
# def login_view(request):
#    redirect_to = request.REQUEST.get('next', '')
#    if request.method=='POST':
#       #create login form...
#       if valid login credentials have been entered:
#          return HttpResponseRedirect(redirect_to)
#    #...
#    return render_to_response('login.html', locals())

def forgotmail(request):
    #Send mail
    print(request.POST['email'], "\n\n")
    if request.method == "POST" :
        form=ForgotPassMailForm(request.POST)
        print(form)
        if form.is_valid():    
            print("Form Validation Successful")
            subject = "Reset Password | Breeze'18"
            message = "You can change your password here:-  "
            from_email = settings.EMAIL_HOST_USER
            print(request.POST['email'])
            to_list = [request.POST['email']]
            print(os.getcwd())
            url_hash= "".join(random.choice(string.ascii_letters + string.digits) for _ in range(64))
            try:
                user=User.objects.filter(email=request.POST['email'].strip())[0]
                print("user=",user)
                ForgetPass.objects.create(token=url_hash,user=user)                
            except:
                return HttpResponseRedirect('/#passwordreseterror')

            html_message = loader.render_to_string(
                os.getcwd()+'/Breeze/templates/mails/ForgotPassword.html',
                {
                    # 'name' : name,
                    'email' : request.POST['email'],
                    'hash' : url_hash,
                    'siteName': "http://snu-breeze.com/forgotPassword",
                    # 'user_name': username,
                    # 'subject': 'Thank you for registering with us '+username+' \n You will now be recieving Notifications for howabouts at SNU in an all new Way. Goodbye to the spam mails. \n Thanks for registering. Have a nice day!!',
                    # 'linkTosite': 'www.google.com',
                }
            )
            try:
                send_mail(subject, message, "Breeze'18 "+from_email, to_list, fail_silently=False, html_message=html_message)                
            except Exception as e:
                print("Mail not sent")
                print (e.message, e.args)
            # return render(request, 'forgotPass.html')
            return HttpResponseRedirect("/#mailsent")
        else:
            raise forms.ValidationError("Form can not be Validated.")

def forgot(request,hashkey):

    next = ""
    if request.GET:
        next = request.GET['next']
        
    if request.method == "POST":
        form = ForgotPassForm(request.POST)
        print("IDSIFOABDOA SDIASJOD ASJDIO ASJDJ ADISJ OIADJOIASD\n\n")
        # print(form)
        # print(form.get('name'))
        print(form)
        if form.is_valid():
            print("VALIDATION SUCCESSFUL")
            userObj = form.cleaned_data
            password =userObj['password']
            confirm = userObj['confirmpass']
            print(" password and confirmpassword is as follows:- ",password,confirm,"\n\n\n\n")
            if(password==confirm):
                # subject = "Registration for Breeze 18 successful."
                # message = "Welcome to Breeze 18 by SNU. "
                # from_email = settings.EMAIL_HOST_USER
                # to_list = [email]
                try:
                    #Change Password
                    user = ForgetPass.objects.filter(token=hashkey)[0]
                    print(user)
                    user = user.user
                    user.set_password(password)
                    user.save()
                    #Delete instance from Table
                    ForgetPass.objects.filter(token=hashkey).delete()
                    print("Password Changed Successfully")
                    return HttpResponseRedirect("/#passwordresetsuccess")
                except:
                    raise forms.ValidationError("Unable to Change Password")

            else:
                return HttpResponseRedirect(next)
    else:
        if(len(hashkey)!=64):
            return HttpResponseRedirect('/#404')
        #print("Hello There")
        forget_pass_object = ForgetPass.objects.filter(token=hashkey)
        if not forget_pass_object:
            return HttpResponseRedirect('/#404')
        #print(forget_pass_object)
        return render(request, "forgotPass.html", {"hashkey" : hashkey})
