from datetime import datetime, timedelta

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from myapp.models import *


def login(request):
    return render(request,'loginindex.html')

def login_post(request):
    username=request.POST['textfield']
    password=request.POST['textfield2']

    l =Login.objects.filter(username=username, password=password)
    if l.exists():
        ll =Login.objects.get(username=username, password=password)
        request.session['lid']=ll.id
        if ll.type == "admin":
            return HttpResponse('''<script>alert('Welcome !!');window.location="/myapp/adminhome/"</script>''')
        elif ll.type == "Bussiness":
            return HttpResponse('''<script>alert('Welcome !!');window.location="/myapp/bussinesshome/"</script>''')

        else:
            return HttpResponse('''<script>alert('Invalid Credentials !! USer Not Found !!');window.location="/myapp/login/"</script>''')
    else:
        return HttpResponse('''<script>alert('Invalid Credentials !! USer Not Found !!');window.location="/myapp/login/"</script>''')


def changepass(request):
    return render(request,'Admin/change pass.html')

def changepass_post(request):
    currentpass=request.POST['textfield']
    newpass=request.POST['textfield2']
    confirmpass=request.POST['textfield3']

    lid=request.session['lid']
    p = Login.objects.get(id=lid)

    if p.password == currentpass:
        if newpass == confirmpass:
            p.password =confirmpass
            p.save()
            return HttpResponse('''<script>alert('Password Changed Successfully !!');window.location="/myapp/login/"</script>''')
        else:
            return HttpResponse('''<script>alert('Passwords do not match !!');history.back()</script>''')
    else:
        return HttpResponse('''<script>alert('Current Password do not match !!');history.back()</script>''')



def viewbusinesapprorej(request):
    v=Bussiness.objects.filter(status='pending')
    return render(request,'Admin/view buss,appr or rejet.html',{'data':v})

def viewbusinesapprorej_post(request):
    search=request.POST['textfield']
    v = Bussiness.objects.filter(status='pending',name__icontains=search)
    return render(request, 'Admin/view buss,appr or rejet.html', {'data': v})


def approve(request,id):
    from datetime import datetime
    r=Bussiness.objects.filter(LOGIN_id = id).update(status = 'approved',date = datetime.now().strftime("%Y-%m-%d"))
    t=Login.objects.filter(id = id ).update(type='Bussiness')
    return HttpResponse('''<script>alert('Approve Successfully !!');window.location="/myapp/viewbusinesapprorej/"</script>''')

def reject(request,id):
    from datetime import datetime
    v=Bussiness.objects.filter(LOGIN_id = id).update(status = 'rejected',date = datetime.now().strftime("%Y%m%d"))
    j=Login.objects.filter(id = id ).update(type = 'reject')
    return HttpResponse('''<script>alert('Rejected Successfully !!');window.location="/myapp/viewbusinesapprorej/"</script>''')


def viewapprobusines(request):
    v=Bussiness.objects.filter(status='approved')
    return render(request,'Admin/view appro bussines.html',{'data':v})

def viewapprobusines_post(request):
    search = request.POST['textfield']
    v=Bussiness.objects.filter(status='approved',name__icontains=search)
    return render(request, 'Admin/view appro bussines.html',{'data':v})


def viewrejectbusines(request):
    v=Bussiness.objects.filter(status='rejected')
    return render(request,'Admin/view rejected bussines.html',{'data':v})

def viewrejectbusines_post(request):
    search = request.POST['textfield']

    v=Bussiness.objects.filter(status='rejected',name__icontains=search)

    return render(request, 'Admin/view rejected bussines.html',{'data':v})


def viewuser(request):
    v=User.objects.all()
    return render(request,'Admin/view user.html',{'data':v})

def viewuser_post(request):
    return render(request,'Admin/view user.html')


def sendnotifi(request):
    return render(request,'Admin/send notification admin.html')

def sendnotifi_post(request):
    notification=request.POST['textarea']
    import datetime
    n=AppNotification()
    n.message=notification
    n.date=datetime.datetime.now().date()
    n.time=datetime.datetime.now().time()
    n.save()
    return HttpResponse('''<script>alert('Notification Send Successfully !!');window.location="/myapp/adminhome/"</script>''')


def viewfeedapp(request):
    var = FeedbackApp.objects.filter(FROM__type='User')
    return render(request,'Admin/view feedback about app from user.html',{'data' : var})

def viewfeedapp_post(request):
    fromdate=request.POST['textfield']
    todate=request.POST['textfield2']

    var = FeedbackApp.objects.filter(date__range=[fromdate,todate])

    return render(request, 'Admin/view feedback about app from user.html',{'data':var})


def viewfeedbusines(request):
    var = FeedbackBussiness.objects.all()

    return render(request,'Admin/view feedback about business.html',{'data':var})

def viewfeedbusines_post(request):
    search=request.POST['textfield7']
    fromdate=request.POST['textfield']
    todate=request.POST['textfield2']
    print(search)

    if search=="":
        var = FeedbackBussiness.objects.filter(date__range=[fromdate, todate])
        return render(request, 'Admin/view feedback about business.html', {'data': var})
    else:
        var = FeedbackBussiness.objects.filter(BUSSINESS__name__icontains=search)
        return render(request, 'Admin/view feedback about business.html',{'data':var})



def viewfeedfrmbusines(request):
    var = FeedbackApp.objects.filter(FROM__type='Bussiness')

    return render(request,'Admin/view feedback from busines.html' ,{'data':var})

def viewfeedfrmbusines_post(request):
    fromdate=request.POST['textfield']
    todate=request.POST['textfield2']
    var = FeedbackApp.objects.filter(date__range=[fromdate,todate])

    return render(request, 'Admin/view feedback from busines.html' , {'data':var})

def adminhome(request):
    return render(request,'Admin/index.html')





def signup(request):
    return render(request,'Business/signup.html')

def signup_post(request):
    name=request.POST['textfield']
    city=request.POST['textfield2']

    district=request.POST['textfield3']
    state = request.POST['textfield4']
    pin = request.POST['textfield5']
    post = request.POST['textfield6']
    phone=request.POST['textfield7']
    email=request.POST['textfield10']
    idproof=request.FILES['fileField']
    logo=request.FILES['fileField2']
    propname=request.POST['textfield13']
    propphoto=request.FILES['fileField3']
    propemail=request.POST['textfield14']
    propphone=request.POST['textfield15']
    website=request.POST['textfield16']
    openingtime=request.POST['textfield11']
    closingtime=request.POST['textfield12']
    password=request.POST['textfield8']
    cpassword=request.POST['textfield9']

    if password != cpassword:
        return HttpResponse('''<script>alert('Passwords do not match !!');history.back()</script>''')

    if Login.objects.filter(username=email).exists():
        return HttpResponse('''<script>alert('Mail already exists !!');history.back()</script>''')

    fs=FileSystemStorage()
    date=datetime.now().strftime("%Y%m%d-%H%M%S")+".jpg"
    fs.save(date,propphoto)
    path=fs.url(date)

    date1 = datetime.now().strftime("%Y%m%d-%H%M%S")+"1.jpg"
    fs.save(date1, logo)
    path1 = fs.url(date1)

    date2 = datetime.now().strftime("%Y%m%d-%H%M%S")+"2.jpg"
    fs.save(date2, idproof)
    path2 = fs.url(date2)



    l=Login()
    l.username=email
    l.password=password
    l.type='pending'
    l.save()

    b=Bussiness()
    b.name=name
    b.city=city
    b.district=district
    b.state=state
    b.pincode=pin
    b.post=post
    b.phone=phone
    b.email=email
    b.idproof=path2
    b.photo=path1
    b.propname=propname
    b.propphoto=path
    b.propemail=propemail
    b.propphone=propphone
    b.website=website
    b.openingtime=openingtime
    b.closingtime=closingtime
    b.status="pending"
    b.LOGIN=l
    b.date=datetime.now().date()
    b.save()


    return HttpResponse('''<script>alert('Successfully Registered !!');window.location="/myapp/login/"</script>''')

def changepassbussi(request):
    return render(request,'Business/change pass bussiness.html')

def changepassbussi_post(request):
    currentpass=request.POST['textfield']
    newpass=request.POST['textfield2']
    confirmpass=request.POST['textfield3']

    lid=request.session['lid']
    p = Login.objects.get(id=lid)

    if p.password == currentpass:
        if newpass == confirmpass:
            p.password =confirmpass
            p.save()
            return HttpResponse('''<script>alert('Password Changed Successfully !!');window.location="/myapp/login/"</script>''')
        else:
            return HttpResponse('''<script>alert('Invalid User Name !!');window.location="/myapp/login/"</script>''')
    else:
        return HttpResponse('''<script>alert('Password Not Match !!');window.location="/myapp/login/"</script>''')



def viewprofile(request):
    res=Bussiness.objects.get(LOGIN_id=request.session['lid'])
    return render(request,'Business/View profile.html',{'i':res})


def editprofile(request):
    res=Bussiness.objects.get(LOGIN_id=request.session['lid'])
    return render(request,'Business/edit profile.html',{'i':res})

def editprofile_post(request):
    name = request.POST['textfield']
    city = request.POST['textfield2']
    district = request.POST['textfield3']
    state = request.POST['textfield4']
    pin = request.POST['textfield5']
    post = request.POST['textfield6']
    phone = request.POST['textfield7']
    email = request.POST['textfield8']
    propname = request.POST['textfield11']
    propemail = request.POST['textfield12']
    propphone = request.POST['textfield13']
    website = request.POST['textfield14']
    openingtime = request.POST['textfield9']
    closingtime = request.POST['textfield10']
    id=request.session['lid']




    if 'fileField2' in request.FILES:
        idproof = request.FILES['fileField2']
        if idproof !='':
            fs = FileSystemStorage()
            date = datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
            fs.save(date, idproof)
            path = fs.url(date)
            b = Bussiness.objects.get(LOGIN_id=id)
            b.idproof=path
            b.save()
    if 'fileField'in request.FILES:
        logo = request.FILES['fileField']
        if logo!='':
            fs1 = FileSystemStorage()
            date1 = datetime.now().strftime("%Y%m%d-%H%M%S") + "1.jpg"
            fs1.save(date1, logo)
            path1 = fs1.url(date1)
            b = Bussiness.objects.get(LOGIN_id=id)
            b.photo = path1
            b.save()

    if 'fileField3'in request.FILES:
        propphoto = request.FILES['fileField3']
        if propphoto!='':
            fs2 = FileSystemStorage()
            date1 = datetime.now().strftime("%Y%m%d-%H%M%S") + "1.jpg"
            fs2.save(date1, propphoto)
            path2 = fs2.url(date1)
            b = Bussiness.objects.get(LOGIN_id=id)
            b.idproof = path2
            b.save()





    b = Bussiness.objects.get(LOGIN_id=id)
    b.name = name
    b.city = city
    b.district = district
    b.state = state
    b.pincode = pin
    b.post = post
    b.phone = phone
    b.email = email
    b.propname = propname
    b.propemail = propemail
    b.propphone = propphone
    b.website = website
    b.openingtime = openingtime
    b.closingtime = closingtime
    b.save()

    return HttpResponse('''<script>alert('Updated Successfully !!');window.location="/myapp/viewprofile/"</script>''')


def addslot(request):
    return render(request,'Business/add slot.html')

def addslot_post(request):
    # slotnum=request.POST['textfield']
    # stno=int(slotnum)
    date = request.POST['textfield1']
    timefrom = request.POST['textfield2']
    timeto = request.POST['textfield3']
    strttime = datetime.strptime(timefrom, "%H:%M")
    endtime = datetime.strptime(timeto, "%H:%M")
    slot = []
    current_time = strttime

    existing_slots = Slot.objects.filter(
        date=date,
        fromtime__gte=strttime.strftime("%I:%M %p"),
        totime__lte=endtime.strftime("%I:%M %p"),
        BUSSINESS__LOGIN_id=request.session['lid']
    )

    if existing_slots.exists():

        print("Slots already exist for the given date and time range. Skipping creation.")
    else:
        while current_time < endtime:
            slot_end_time = current_time + timedelta(minutes=15)
            slot.append((current_time.strftime("%I:%M %p"), slot_end_time.strftime("%I:%M %p")))
            current_time = slot_end_time

        start = 1
        exSlot = Slot.objects.filter(BUSSINESS__LOGIN_id=request.session['lid'], date=date).order_by('-id')
        # exSlot = Slot.objects.filter(BUSSINESS__LOGIN_id=request.session['lid']).order_by('-id')
        if exSlot.exists():
            start = exSlot[0].number + 1
        for index, slot in enumerate(slot, start=start):
            print(f"Slot {index}:{slot[0]}-{slot[1]}")
            obj = Slot()
            obj.number = index
            obj.date = date
            obj.fromtime = slot[0]
            obj.totime = slot[1]
            obj.BUSSINESS = Bussiness.objects.get(LOGIN=request.session['lid'])
            obj.expectedtime = slot[0]
            obj.save()
    return HttpResponse('''<script>alert('Slot Number Added !!');window.location="/myapp/bussinesshome/"</script>''')



def viewslot(request):
    var=Slot.objects.filter(BUSSINESS__LOGIN_id=request.session['lid'])
    return render(request,'Business/view slot.html',{'data':var})

def deleteslot(request,id):
    var=Slot.objects.get(id=id).delete()
    return HttpResponse('''<script>alert('Slot Number Deleted Successfully !!');window.location="/myapp/viewslot/"</script>''')


def confirmslotreq(request):
    var=BookingRequest.objects.filter(status='pending', SLOT__BUSSINESS__LOGIN_id= request.session['lid'])
    return render(request,'Business/confirm usertime slot request.html',{'data':var})

def confirmslotreq_post(request):
    search=request.POST['textfield']
    var=BookingRequest.objects.filter(status='pending',id__icontains=search, SLOT__BUSSINESS__LOGIN_id= request.session['lid'])

    return render(request, 'Business/confirm usertime slot request.html',{'data':var})


def approveslot(request,id):
    var=BookingRequest.objects.filter(id=id)
    var.update(status='approved')
    noti = Notification()
    noti.FROM_id = request.session['lid']
    noti.TO_id = var[0].USER.LOGIN_id
    noti.date = datetime.now().date()
    noti.time = datetime.now().strftime('%H:%M')
    noti.message = 'Slot '+var[0].SLOT.fromtime+ ' to '+var[0].SLOT.totime+' has been approved.'
    noti.type = 'Slot Approval'
    noti.save()
    return HttpResponse('''<script>alert('Slot Number Approved Successfully !!');window.location="/myapp/confirmslotreq/"</script>''')

def rejectslot(request,id):
    var=BookingRequest.objects.filter(id=id).update(status='rejected')
    return HttpResponse('''<script>alert('Slot Number Rejected!!');window.location="/myapp/confirmslotreq/"</script>''')


def viewapproslot(request):
    dt = str(datetime.now().date().today())
    var=BookingRequest.objects.filter(status='approved', SLOT__BUSSINESS__LOGIN_id= request.session['lid'])
    return render(request, 'Business/view approved slots.html',{'data':var, 'dt':dt})

def viewapproslot_post(request):
    search=request.POST['textfield']
    dt = str(datetime.now().date().today())
    var=BookingRequest.objects.filter(status='approved',id__icontains=search, SLOT__BUSSINESS__LOGIN_id= request.session['lid'])
    return render(request, 'Business/view approved slots.html',{'data':var, 'dt':dt})

def viewrejectslot(request):
    var=BookingRequest.objects.filter(status='rejected', SLOT__BUSSINESS__LOGIN_id= request.session['lid'])
    return render(request,'Business/view rejected slots.html',{'data':var})

def viewrejectslot_post(request):
    search=request.POST['textfield']
    var=BookingRequest.objects.filter(status='rejected',id__icontains=search, SLOT__BUSSINESS__LOGIN_id= request.session['lid'])
    return render(request, 'Business/view rejected slots.html',{'data':var})


def sendnotifibusines(request,id):
    return render(request,'Business/send notification bussiness.html',{'id':id})

def sendnotifibusines_post(request):
    notification=request.POST['textarea']
    toid=request.POST['id']
    var = Notification()
    var.FROM_id = request.session['lid']
    var.TO_id = toid
    var.message = notification
    from datetime import datetime
    var.date = datetime.now().date()
    var.time = datetime.now().time()
    var.type = "remainder"
    var.save()

    return HttpResponse('''<script>alert('Notification Send Successfully !!');window.location="/myapp/viewapproslot/"</script>''')


def bussinesshome(request):
    return render(request,'Business/index.html')


def viewnotifi(request):
    var = Notification.objects.filter(FROM_id = request.session['lid'])
    return render(request,'Business/view notification.html',{'data':var})

def viewnotifi_post(request):
    fromdate = request.POST['textfield']
    todate = request.POST['textfield2']
    var = Notification.objects.filter(date__range=[fromdate,todate],FROM_id= request.session['lid'])
    return render(request,'Business/view notification.html',{'data':var})

def deletenotifi(request,id):
    var=Notification.objects.get(id=id).delete()
    return HttpResponse('''<script>alert('Notification Deleted Successfully !!');window.location="/myapp/viewnotifi/"</script>''')



def sendfeed(request):
    return render(request,'Business/send feedback.html')

def sendfeed_post(request):

    rating=request.POST['textfield3']
    review=request.POST['textarea']
    var = FeedbackApp()
    var.rating = rating
    var.review = review
    from datetime import datetime
    var.date = datetime.now().date()
    var.time = datetime.now().time()
    var.FROM_id = request.session['lid']
    var.save()


    return HttpResponse('''<script>alert('Feedback Send Successfully !!');window.location="/myapp/viewnotifi/"</script>''')




def forget_password(request):
    return render(request,'forget password.html')

def forget_password_post(request):
    em = request.POST['em_add']
    import random
    password = random.randint(00000000, 99999999)
    log = Login.objects.filter(username=em)
    if log.exists():
        logg = Login.objects.get(username=em)
        message = 'temporary password is ' + str(password)
        send_mail(
            'temp password',
            message,
            settings.EMAIL_HOST_USER,
            [em, ],
            fail_silently=False
        )
        logg.password = password
        logg.save()
        return HttpResponse('<script>alert("success");window.location="/myapp/login/" </script>')
    else:
        return HttpResponse('<script>alert("invalid email");window.location="/myapp/login/" </script>')



#-----------------------USER---------------------------------------------#


def user_login(request):
    username=request.POST['username']
    password=request.POST['password']
    var=Login.objects.filter(username=username,password=password)
    if var.exists():
        var=Login.objects.get(username=username,password=password)
        if var.type=='User':
            lid=var.id
            return JsonResponse({'status':'ok','lid':str(lid),'type':'User'})
        else :
            return JsonResponse({'status':'no'})
    else :
        return JsonResponse({'status': 'no'})

def user_changepassword(request):
    oldpassword=request.POST['current']
    newpassword=request.POST['new']
    confirmpassword = request.POST['confirm']
    lid = request.POST['lid']
    res=Login.objects.filter(password=oldpassword, id=lid)
    if res.exists():
        if newpassword == confirmpassword:
            res = Login.objects.filter(id=lid, password=oldpassword).update(password=confirmpassword)
            return JsonResponse({"status":"ok"})
        else:
            return JsonResponse({"status":"no"})
    else:
        return JsonResponse({"status":"not"})


def user_signup(request):
    name = request.POST['name']
    gender = request.POST['gender']
    dob = request.POST['dob']
    photo = request.POST['photo']
    email = request.POST['email']
    phone = request.POST['phoneno']
    place = request.POST['place']
    post = request.POST['post']
    pincode = request.POST['pincode']
    password = request.POST['password']
    cpassword =request.POST['confirm_password']

    if password == cpassword:
        if not Login.objects.filter(username=email).exists():
            import base64
            a = base64.b64decode(photo)
            from datetime import datetime
            date = datetime.now().strftime('%Y%m%d-%H%M%S')+ '.jpg'
            fh = open(settings.MEDIA_ROOT+'\\user\\'+date,'wb')
            path = '/media/user/'+date
            fh.write(a)
            fh.close()

            var = Login()

            var.username = email
            var.password = cpassword
            var.type = 'User'
            var.save()

            l = User()
            l.name = name
            l.gender = gender
            l.dob = dob
            l.photo = path
            l.email = email
            l.phone = phone
            l.place = place
            l.post = post
            l.pincode = pincode
            l.LOGIN = var
            l.save()
            return JsonResponse({'status':'ok'})
    return JsonResponse({'status':'no'})


def user_editprofile(request):
    name = request.POST['name']
    gender = request.POST['gender']
    dob = request.POST['dob']
    photo = request.POST['photo']
    email = request.POST['email']
    phone = request.POST['phone']
    place = request.POST['place']
    post = request.POST['post']
    pincode = request.POST['pincode']
    lid = request.POST['lid']
    if len(photo) > 5 :
        import base64
        a = base64.b64decode(photo)
        from datetime import datetime
        date = datetime.now().strftime('%Y%m%d-%H%M%S') + '.jpg'
        fh = open('C:\\Users\\USER\\PycharmProjects\\QueuingApp\\media\\user\\' + date, 'wb')
        path = '/media/user/' + date
        fh.write(a)
        fh.close()
        l = User.objects.get(LOGIN_id = lid)
        l.photo = path
        l.save()

    l = User.objects.get(LOGIN_id = lid)
    l.name = name
    l.gender = gender
    l.dob = dob
    l.email = email
    l.phone = phone
    l.place = place
    l.post = post
    l.pincode = pincode
    l.save()
    return JsonResponse({'status': 'ok'})


def user_viewprofile(request):
    lid = request.POST['lid']
    var = User.objects.get(LOGIN_id = lid)
    return  JsonResponse({'status':'ok','name':var.name, 'gender':var.gender, 'dob':var.dob, 'photo':var.photo, 'email':var.email, 'phone':var.phone,
                          'place':var.place, 'post':var.post, 'pincode':var.pincode})


def user_viewbussiness(request):
    obj = Bussiness.objects.filter(status="approved")
    l = []
    for i in obj:
        l.append({'status':'ok',"id":i.id,'photo':i.photo, 'name':i.name, 'city':i.city, 'district':i.district,
                  'state':i.state, 'pincode':i.pincode, 'post':i.post, 'phone':i.phone, 'email':i.email, 'propname':i.propname,
                   'propemail':i.propemail, 'propphone':i.propphone, 'website':i.website,
                  'openingtime':i.openingtime, 'closingtime':i.closingtime,"blid":i.LOGIN.id})
    return  JsonResponse({'status':'ok',"data":l})


def user_viewbussiness_location(request):
    return  JsonResponse({'status':'ok'})

def user_viewbussiness_byname(request):
    return  JsonResponse({'status':'ok'})

print(BookingRequest.objects.filter().values_list('SLOT__date').distinct())
def user_viewcurrentslot(request):
    bid=request.POST['bid']
    # var = Slot.objects.filter(BUSSINESS__id=bid).order_by('-number')
    bkl = BookingRequest.objects.filter().values_list('SLOT_id', 'SLOT__date')
    try:
        var = Slot.objects.filter(BUSSINESS__id=bid, date__gte=datetime.now().date().today())\
            .exclude(id__in=BookingRequest.objects.filter().values_list('SLOT_id')[0],
                     date__in=BookingRequest.objects.filter().values_list('SLOT__date').distinct()[0]).order_by('-number')
    except:
        var = Slot.objects.filter(BUSSINESS__id=bid, date__gte=datetime.now().date().today()).order_by('-number')
    ctime = datetime.now().strftime('%Y-%m-%d %I:%M %p')
    l = []
    current = '0'
    for i in var:
        if BookingRequest.objects.filter(SLOT_id=i.id).exists():
            continue
        if datetime.strptime(str(i.date)+' '+i.fromtime, '%Y-%m-%d %I:%M %p') > datetime.strptime(ctime, '%Y-%m-%d %I:%M %p') and str(i.date) >= str(datetime.now().date()):
            if ctime>=i.fromtime and ctime<=i.totime and str(i.date) == str(datetime.now().date()):
                current = i.number
            l.append({'id':i.id,'number':i.number, 'date':i.date, 'fromtime':i.fromtime, 'totime':i.totime})
    print(l)
    return  JsonResponse({'status':'ok',"data":l, 'current': current})

def user_bookslot(request):
    lid = request.POST['lid']
    sid = request.POST['sid']
    obj = BookingRequest()
    obj.USER=User.objects.get(LOGIN__id=lid)
    obj.SLOT_id=sid
    obj.date = datetime.now().date().today()
    obj.time = datetime.now().time()
    obj.status = 'pending'
    obj.save()
    return  JsonResponse({'status':'ok'})



def user_view_request(request):
    lid=request.POST['lid']
    res=BookingRequest.objects.filter(USER__LOGIN__id=lid)
    l=[]
    for i in res:
        l.append({'id': i.id, 'number': i.SLOT.number, 'date': i.SLOT.date, 'fromtime': i.SLOT.fromtime, 'totime': i.SLOT.totime,"bname":i.SLOT.BUSSINESS.name,"bstatus":i.status,"expectedtime":i.SLOT.expectedtime})
    return JsonResponse({'status': 'ok', "data": l})

def user_view_request_home(request):
    lid=request.POST['lid']
    from django.db.models import Q
    res=BookingRequest.objects.filter(Q(status__icontains='approved')| Q(status__icontains='pending'),USER__LOGIN__id=lid, date__gte=datetime.now().date())
    l=[]
    for i in res:
        cslt = ''
        if BookingRequest.objects.filter(status='Completed', SLOT__date=datetime.now().date(), SLOT__BUSSINESS=i.SLOT.BUSSINESS).exists():
            cslt = BookingRequest.objects.filter(status='Completed', SLOT__date=datetime.now().date(), SLOT__BUSSINESS=i.SLOT.BUSSINESS)[0].SLOT.number
        l.append({'id': i.id, 'number': i.SLOT.number, 'date': i.SLOT.date, 'fromtime': i.SLOT.fromtime, 'totime': i.SLOT.totime,"bname":i.SLOT.BUSSINESS.name,"bstatus":i.status,"expectedtime":i.SLOT.expectedtime, 'cslt':cslt})
    return JsonResponse({'status': 'ok', "data": l})


def user_viewestimated_waittime(request):
    return  JsonResponse({'status':'ok'})

def user_viewrealtime_updation(request):
    return  JsonResponse({'status':'ok'})


def user_view_notification(request):
    return  JsonResponse({'status':'ok'})


def user_chat(request):
    return  JsonResponse({'status':'ok'})

def user_feedbackbussiness(request):
    lid = request.POST['lid']
    bid = request.POST['bid']
    feedback = request.POST['feedback']
    from datetime import datetime
    date = datetime.now().date().today()
    var = FeedbackBussiness()
    var.date=date
    var.time = datetime.now().strftime('%H:%M:%S')
    var.BUSSINESS_id=bid
    var.CUSTOMER = User.objects.get(LOGIN_id = lid)
    var.save()
    return  JsonResponse({'status':'ok'})

def user_feedbackapp(request):
    lid = request.POST['lid']
    review = request.POST['complaint']
    obj = FeedbackApp()
    obj.date = datetime.now().date().today()
    obj.time = datetime.now().time()
    obj.FROM = Login.objects.get(id = lid)
    obj.review = review
    obj.save()
    return  JsonResponse({'status':'ok'})



# def business_updatestatus(request,sid):
    # lid=request.session['lid']
    # res=BookingRequest.objects.filter(id=sid,SLOT__BUSSINESS__LOGIN__id=lid).update(status="finish")
    # aa = BookingRequest.objects.get(id=sid, SLOT__BUSSINESS__LOGIN__id=lid)
    # currenttime=datetime.now().strftime("%I:%M %p")
    # fromtime=aa.SLOT.fromtime
    # totime=aa.SLOT.totime
    # slotid=aa.SLOT.id
    #
    # print(currenttime,"Jjjjjjjjjjjjj")
    # time1=datetime.strptime(currenttime,"%I:%M %p")
    # print(time1,"kkkkkkkkkkk")
    #
    # time2=datetime.strptime(totime,"%I:%M %p")
    # print(time2,"-------------",time1)
    # print(type(time2),type(time1))
    # time_diff=(time2-time1).total_seconds()/60
    # print(time_diff,"hhhhh")
    # s=Slot.objects.filter(id__lte=slotid)
    # for i in s:
    #     sm=i. expectedtime
    #     time2 = datetime.strptime(sm, "%I:%M %p")
    #
    #
    #
    #     if time_diff > 0 :
    #         time3 = datetime(minute=int(time_diff), year=2001, month=1, day=1)
    #         at = time2 + time3
    #         i.expectedtime=at
    #         i.save()
    #     else:
    #
    #         time_diff= time_diff*-1
    #
    #
    #         time3 = datetime(minute=int(time_diff), year=2001, month=1, day=1)
    #         # at = time2 + time3
    #         ac=time2-time3
    #         i.expectedtime=ac
    #         i.save()
    # # ab=str(aa.SLOT.totime)-str(time_diff)
    # # print(ab,"hhhhh")

    # return HttpResponse('''<script>alert('Updated Successfully !!');window.location="/myapp/viewapproslot/"</script>''')


from datetime import datetime, timedelta
from django.http import HttpResponse
from django.shortcuts import redirect


# def finish_booking(request, sid):
#     if 'lid' in request.session:
#         lid = request.session['lid']
#
#         # Update booking request status to "finish"
#         BookingRequest.objects.filter(id=sid, SLOT__BUSSINESS__LOGIN__id=lid).update(status="finish")
#
#         # Get the booking request
#         aa = BookingRequest.objects.get(id=sid, SLOT__BUSSINESS__LOGIN__id=lid)
#
#         currenttime = datetime.now()
#         fromtime = datetime.strptime(aa.SLOT.fromtime, "%I:%M %p")
#         totime = datetime.strptime(aa.SLOT.totime, "%I:%M %p")
#         ctm = datetime.strptime(str(datetime.now().strftime('%I:%M %p')), "%I:%M %p")
#         slotid = aa.SLOT.id
#
#         time_diff = (totime - currenttime).total_seconds()/60
#         # time_diff_days = (((currenttime - totime).days))
#         # print(time_diff_days, totime)
#         # print(currenttime, "Time Difference", timedelta(minutes=-time_diff,))
#         print(currenttime, "Time Difference", timedelta(minutes=-time_diff))
#
#         # Update expected times for slots
#         slots = Slot.objects.filter(id__gte=slotid)
#
#         for slot in slots:
#             sm = datetime.strptime(slot.expectedtime, "%I:%M %p")
#
#             if time_diff > 0:
#                 new_expected_time = currenttime + timedelta(minutes=time_diff)
#             else:
#                 new_expected_time = currenttime - timedelta(minutes=-time_diff)
#
#             print(new_expected_time.strftime("%I:%M %p"))
#             slot.expectedtime = new_expected_time.strftime("%I:%M %p")
#             # slot.save()
#         aa.status = 'Completed'
#         aa.save()
#         return HttpResponse("Booking finished successfully!")
#
#     else:
#         return HttpResponse("Session variable 'lid' not found", status=400)

def finish_booking(request, sid):
    if 'lid' in request.session:
        lid = request.session['lid']

        BookingRequest.objects.filter(id=sid, SLOT__BUSSINESS__LOGIN__id=lid).update(status="finish")

        aa = BookingRequest.objects.get(id=sid, SLOT__BUSSINESS__LOGIN__id=lid)

        current_time = datetime.now()
        time_obj = datetime.strptime(aa.SLOT.totime, "%I:%M %p")
        # time_obj = datetime.strptime(aa.SLOT.totime, "%I:%M %p")
        formatted_time_str = time_obj.strftime("%H:%M:%S.%f")

        totime = datetime.strptime(str(aa.SLOT.date)+' '+formatted_time_str, "%Y-%m-%d %H:%M:%S.%f")
        time_diff = (totime - current_time).total_seconds()/60

        slots = Slot.objects.filter(id__gt=aa.SLOT.id, date__gte=datetime.now().date()).order_by('id')

        for slot in slots:
            time_objw = datetime.strptime(slot.expectedtime, "%I:%M %p")
            formatted_time_strw = time_objw.strftime("%H:%M:%S.%f")

            expected_time = datetime.strptime(str(aa.SLOT.date)+' '+formatted_time_strw, "%Y-%m-%d %H:%M:%S.%f")

            new_expected_time = expected_time - timedelta(minutes=time_diff)

            # if current_time > totime:
            #     print("New expected time is greater than to time")
            #     new_expected_time = expected_time + timedelta(minutes=time_diff)
            # elif current_time < totime:
            #     new_expected_time = expected_time - timedelta(minutes=time_diff)
            #     print("New expected time is less than to time")
            # else:
            #     print("New expected time is equal to current time")

            print(new_expected_time.strftime("%Y-%m-%d %H:%M:%S"))

            slot.expectedtime = new_expected_time.strftime('%I:%M %p')
            slot.save()


        aa.status = 'Completed'
        aa.save()
        return HttpResponse('''<script>alert("Booking finished successfully!"); window.location='/myapp/viewapproslot/'</script>''')

    else:
        return HttpResponse('''<script>alert("Please try again!"); window.location='/myapp/viewapproslot/'</script>''')

from datetime import datetime, timedelta


def cancel_slot(request):
    if 'lid' in request.POST:
        sid = request.POST['rid']
        lid = request.POST['lid']

        # Update booking request status to "cancel"
        BookingRequest.objects.filter(id=sid).update(status="Cancelled")

        # Get the booking request
        aa = BookingRequest.objects.get(id=sid)

        currenttime = datetime.now()
        fromtime = datetime.strptime(aa.SLOT.fromtime, "%I:%M %p")
        totime = datetime.strptime(aa.SLOT.totime, "%I:%M %p")
        slotid = aa.SLOT.id

        print(currenttime, "Current Time")
        print(fromtime, "From Time")
        print(totime, "To Time")

        print(totime - fromtime)

        time_diff = (totime - currenttime).total_seconds() / 60
        print(time_diff, "Time Difference")

        # Calculate the time difference between the canceled slot's end time and the next slot's expected start time
        next_slots = Slot.objects.filter(id__gte=slotid, date__gte=datetime.now().date()).order_by('id')

        for slot in next_slots:
            sm = datetime.strptime(str(slot.expectedtime), "%I:%M %p")

            if time_diff > 0:
                new_expected_time = currenttime + timedelta(minutes=time_diff)
            else:
                new_expected_time = currenttime - timedelta(minutes=-time_diff)
            start_time = datetime.strptime(slot.fromtime, "%I:%M %p")
            end_time = datetime.strptime(slot.totime, "%I:%M %p")

            time_difference = end_time - start_time

            time_difference_minutes = time_difference.total_seconds() / 60
            print(time_difference_minutes)
            time_duration_parts = str(time_difference).split(':')
            print(time_duration_parts)
            time_duration = timedelta(
                hours=int(time_duration_parts[0].split('.')[0]),
                                      minutes=int(time_duration_parts[1]),
                                      seconds=int(time_duration_parts[2]))

            # Subtract the time duration from the given time to get the result time
            print(sm, time_duration, time_duration)
            print(sm - time_difference, 'rrrr')
            result_time = str(sm - time_difference).split(' ')[1]
            time_obj = datetime.strptime(result_time, "%H:%M:%S")

            formatted_time_str = time_obj.strftime("%I:%M %p")

            slot.expectedtime = formatted_time_str
            slot.save()
        aa.status = 'Cancelled'
        aa.save()

        print("Slot canceled successfully!")
        return JsonResponse({'status':'ok'})
    return JsonResponse({'status': 'ok'})


# def cancel_request(request):
#     rid=request.POST['rid']
#     lid = request.POST['lid']
#     res = BookingRequest.objects.filter(id=rid,USER__LOGIN__id=lid).update(status="cancel")
#     return HttpResponse('''<script>alert('Updated Successfully !!');window.location="/myapp/viewapproslot/"</script>''')


#####3 chat############################


def chat(request, id):
    request.session["userid"] = id
    cid = str(request.session["userid"])
    request.session["new"] = cid
    qry = User.objects.get(LOGIN_id=cid)

    return render(request, "Business/Chat.html", {'photo': qry.photo, 'name': qry.name, 'toid': cid})


def chat_view(request):
    fromid = request.session["lid"]
    toid = request.session["userid"]
    qry = User.objects.get(LOGIN_id=request.session["userid"])
    from django.db.models import Q

    res = Chat.objects.filter(Q(FROM=fromid, TO=toid) | Q(FROM=toid, TO=fromid))
    l = []

    for i in res:
        l.append({"id": i.id, "message": i.message, "to": i.TO_id, "date": i.date, "from": i.FROM_id})

    return JsonResponse({'photo': qry.photo, "data": l, 'name': qry.name, 'toid': request.session["userid"]})


def chat_send(request, msg):
    lid = request.session["lid"]
    toid = request.session["userid"]
    message = msg

    import datetime
    d = datetime.datetime.now().date()
    chatobt = Chat()
    chatobt.message = message
    chatobt.TO_id = toid
    chatobt.FROM_id = lid
    chatobt.time = datetime.datetime.now().time()
    chatobt.date = d
    chatobt.save()

    return JsonResponse({"status": "ok"})















def user_sendchat(request):
    FROM_id=request.POST['from_id']
    TOID_id=request.POST['to_id']
    # print(FROM_id, TOID_id,"Lk")
    msg=request.POST['message']
    from  datetime import datetime
    c=Chat()
    c.FROM_id=FROM_id
    c.TO_id=TOID_id
    c.message=msg
    c.date=datetime.now().date()
    c.time=datetime.now().time()
    c.save()
    return JsonResponse({'status':"ok"})


def user_viewchat(request):
    fromid = request.POST["from_id"]
    toid = request.POST["to_id"]
    # lmid = request.POST["lastmsgid"]
    print(fromid)
    print(toid)
    from django.db.models import Q

    res = Chat.objects.filter(Q(FROM_id=fromid, TO_id=toid) | Q(FROM_id=toid, TO_id=fromid))
    l = []
    for i in res:
        l.append({"id": i.id, "msg": i.message, "from": i.FROM_id, "date": i.date, "to": i.TO_id})

    return JsonResponse({"status":"ok",'data':l})


def viewNotification(request):
    nid = request.POST["nid"]
    lid = request.POST["lid"]
    res = Notification.objects.filter(id__gt=nid, TO_id=lid)
    l = []
    for i in res:
        l.append({"id": i.id, "msg": i.message, "from": i.FROM_id, "date": i.date, "to": i.TO_id})
        from_ = i.FROM.type
        if from_ != 'admin':
            from_ = Bussiness.objects.get(LOGIN_id=i.FROM.id).name
            if i.type == 'Slot Approval':
                from_ = i.type
        return JsonResponse({"status":"ok",'message':i.message, 'from':from_, 'nid':str(i.id)})
    return JsonResponse({"status":"ok",'data':l, 'nid':nid})
