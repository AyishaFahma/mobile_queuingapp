from datetime import datetime

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
            return HttpResponse('''<script>alert('Invalid User Name !!');window.location="/myapp/login/"</script>''')
    else:
        return HttpResponse('''<script>alert('Password Not Match !!');window.location="/myapp/login/"</script>''')


def viewbusinesapprorej(request):
    v=Bussiness.objects.filter(status='pending')
    return render(request,'Admin/view buss,appr or rejet.html',{'data':v})

def viewbusinesapprorej_post(request):
    search=request.POST['textfield']

    v = Bussiness.objects.filter(status='pending',name__icontains=search)
    return render(request, 'Admin/view buss,appr or rejet.html', {'data': v})



def approve(request,id):
    from datetime import datetime
    r=Bussiness.objects.filter(LOGIN_id = id).update(status = 'approved',date = datetime.now().strftime("%Y%m%d-%H%M%S"))
    t=Login.objects.filter(id = id ).update(type='Bussiness')
    return HttpResponse('''<script>alert('Approve Successfully !!');window.location="/myapp/viewbusinesapprorej/"</script>''')

def reject(request,id):
    from datetime import datetime
    v=Bussiness.objects.filter(LOGIN_id = id).update(status = 'rejected',date = datetime.now().strftime("%Y%m%d-%H%M%S"))
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
    return render(request,'Business/signup page.html')

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
    l.username=name
    l.password=password
    l.type='Bussiness'
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
    slotnum=request.POST['textfield']
    date=request.POST['textfield1']
    timefrom=request.POST['textfield2']
    timeto=request.POST['textfield3']
    obj=Slot()
    obj.number=slotnum
    obj.date=date
    obj.fromtime=timefrom
    obj.totime=timeto
    obj.BUSSINESS=Bussiness.objects.get(LOGIN=request.session['lid'])
    obj.save()
    return HttpResponse('''<script>alert('Slot Number Added !!');window.location="/myapp/bussinesshome/"</script>''')



def viewslot(request):
    var=Slot.objects.all()
    return render(request,'Business/view slot.html',{'data':var})

def deleteslot(request,id):
    var=Slot.objects.get(id=id).delete()
    return HttpResponse('''<script>alert('Slot Number Deleted Successfully !!');window.location="/myapp/viewslot/"</script>''')


def confirmslotreq(request):
    var=BookingRequest.objects.filter(status='pending')
    return render(request,'Business/confirm usertime slot request.html',{'data':var})

def confirmslotreq_post(request):
    search=request.POST['textfield']
    var=BookingRequest.objects.filter(status='pending',id__icontains=search)

    return render(request, 'Business/confirm usertime slot request.html',{'data':var})


def approveslot(request,id):
    var=BookingRequest.objects.filter(id=id).update(status='approved')

    return HttpResponse('''<script>alert('Slot Number Approved Successfully !!');window.location="/myapp/confirmslotreq/"</script>''')

def rejectslot(request,id):
    var=BookingRequest.objects.filter(id=id).update(status='rejected')
    return HttpResponse('''<script>alert('Slot Number Rejected!!');window.location="/myapp/confirmslotreq/"</script>''')


def viewapproslot(request):
    var=BookingRequest.objects.filter(status='approved')
    return render(request,'Business/view approved slots.html',{'data':var})

def viewapproslot_post(request):
    search=request.POST['textfield']
    var=BookingRequest.objects.filter(status='approved',id__icontains=search)
    return render(request, 'Business/view approved slots.html',{'data':var})

def viewrejectslot(request):
    var=BookingRequest.objects.filter(status='rejected')
    return render(request,'Business/view rejected slots.html',{'data':var})

def viewrejectslot_post(request):
    search=request.POST['textfield']
    var=BookingRequest.objects.filter(status='rejected',id__icontains=search)
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
    return render(request,'Business/bussinesshome.html')


def viewnotifi(request):
    var = Notification.objects.all()
    return render(request,'Business/view notification.html',{'data':var})

def viewnotifi_post(request):
    fromdate = request.POST['textfield']
    todate = request.POST['textfield2']
    var = Notification.objects.filter(date__range=[fromdate,todate])
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
    oldpassword=request.POST['oldpassword']
    newpassword=request.POST['newpassword']
    confirmpassword = request.POST['cp']
    lid = request.POST['lid']
    res = Login.objects.filter(id =lid,password=oldpassword)
    if res.exists():
        log = Login.objects.get(id =lid,password=oldpassword)
        if log is not None:
            if newpassword == confirmpassword:
                log = Login.objects.filter(id =lid,password = oldpassword).update(password=confirmpassword)
                return JsonResponse({'staus':'ok'})
            else :
                return JsonResponse({'staus':'not ok'})
        else :
            return JsonResponse({'staus': 'not ok'})
    else :
        return JsonResponse({'staus': 'not ok'})


def user_signup(request):
    name = request.POST['name']
    gender = request.POST['gender']
    dob = request.POST['dob']
    photo = request.POST['photo']
    email = request.POST['email']
    phone = request.POST['phone']
    place = request.POST['place']
    post = request.POST['post']
    pincode = request.POST['pincode']
    password = request.POST['password']
    cpassword =request.POST['cpassword']

    import base64
    a = base64.b64decode(photo)
    from datetime import datetime
    date = datetime.now().strftime('%Y%m%d-%H%M%S')+ '.jpg'
    fh = open('C:\\Users\\USER\\PycharmProjects\\QueuingApp\\media\\user\\'+date,'wb')
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
        l.append({'status':'ok','photo':i.photo, 'name':i.name, 'city':i.city, 'district':i.district,
                  'state':i.state, 'pincode':i.pincode, 'post':i.post, 'phone':i.phone, 'email':i.email, 'propname':i.propname,
                   'propemail':i.propemail, 'propphone':i.propphone, 'website':i.website,
                  'openingtime':i.openingtime, 'closingtime':i.closingtime})
    return  JsonResponse({'status':'ok',"data":l})





def user_viewbussiness_location(request):
    return  JsonResponse({'status':'ok'})

def user_viewbussiness_byname(request):
    return  JsonResponse({'status':'ok'})




def user_viewcurrentslot(request):
    bid=request.POST['bid']
    var = Slot.objects.filter(BUSSINESS__id=bid)
    l = []
    for i in var:
        l.append({'id':i.id,'number':i.number, 'date':i.date, 'fromtime':i.fromtime, 'totime':i.totime})
    return  JsonResponse({'status':'ok',"data":l})

def user_bookslot(request):
    lid = request.POST['lid']
    sid = request.POST['sid']
    obj = BookingRequest()
    obj.date = datetime.now().date().today()
    obj.time = datetime.now().strftime()
    obj.status = 'pending'
    obj.save()
    return  JsonResponse({'status':'ok'})

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
    review = request.POST['review']
    rating = request.POST['rating']
    obj = FeedbackApp()
    obj.date = datetime.now().date().today()
    obj.time = datetime.now().strftime()
    obj.FROM = Login.objects.get(id = lid)
    obj.review = review
    obj.rating = rating
    obj.save()
    return  JsonResponse({'status':'ok'})






























