from django.db import models

# Create your models here.

class Login(models.Model):
    username =models.CharField(max_length=100)
    password =models.CharField(max_length=100)
    type =models.CharField(max_length=100)

class Bussiness(models.Model):
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)
    photo =models.CharField(max_length=500)
    name =models.CharField(max_length=100)
    idproof =models.CharField(max_length=500)
    city =models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode= models.IntegerField()
    post = models.CharField(max_length=100)
    phone = models.BigIntegerField()
    email = models.CharField(max_length=100)
    propname = models.CharField(max_length=100)
    propphoto = models.CharField(max_length=500)
    propemail = models.CharField(max_length=100)
    propphone = models.BigIntegerField()
    website = models.CharField(max_length=100)
    openingtime = models.CharField(max_length=100)
    closingtime = models.CharField(max_length=100)
    status = models.CharField(max_length=100,default=0)
    date = models.DateField()



class User(models.Model):
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    dob = models.DateField()
    photo = models.CharField(max_length=500)
    email = models.CharField(max_length=100)
    phone = models.BigIntegerField()
    place = models.CharField(max_length=100)
    post = models.CharField(max_length=100)
    pincode = models.IntegerField()


class Slot(models.Model):
    BUSSINESS = models.ForeignKey(Bussiness,on_delete=models.CASCADE)
    number = models.IntegerField()
    date=models.DateField()
    fromtime = models.CharField(max_length=100,default="")
    totime = models.CharField(max_length=100,default="")
    expectedtime = models.CharField(max_length=100,default="")


class BookingRequest(models.Model):
    USER = models.ForeignKey(User,on_delete=models.CASCADE)
    SLOT = models.ForeignKey(Slot,on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=100,default='pending')

class Notification(models.Model):
    FROM = models.ForeignKey(Login,on_delete=models.CASCADE,related_name="from1")
    TO = models.ForeignKey(Login,on_delete=models.CASCADE,related_name="to1")
    message = models.CharField(max_length=900)
    date = models.DateField()
    time = models.TimeField()
    type = models.CharField(max_length=400)

class Chat(models.Model):
    FROM = models.ForeignKey(Login,on_delete=models.CASCADE,related_name="bussiness1")
    TO = models.ForeignKey(Login,on_delete=models.CASCADE,related_name="customer1")
    message = models.CharField(max_length=900)
    date = models.DateField()
    time = models.TimeField()

class FeedbackApp(models.Model):
    FROM = models.ForeignKey(Login, on_delete=models.CASCADE)
    review = models.CharField(max_length=900)
    date = models.DateField()
    time = models.TimeField()


class FeedbackBussiness(models.Model):
    CUSTOMER = models.ForeignKey(User,on_delete=models.CASCADE)
    BUSSINESS = models.ForeignKey(Bussiness,on_delete=models.CASCADE)
    review = models.CharField(max_length=900)
    date = models.DateField()
    time = models.TimeField()
    rating = models.CharField(max_length=100)


class AppNotification(models.Model):
    message = models.CharField(max_length=900)
    date = models.DateField()
    time = models.TimeField()


# class Reply(models.Model):
#     FROM = models.ForeignKey(Login,on_delete=models.CASCADE,related_name="from")
#     TO = models.ForeignKey(Login,on_delete=models.CASCADE,related_name="to")
#     subject = models.CharField(max_length=500)
#     message = models.CharField(max_length=800)
#     date = models.DateField()
#     time = models.TimeField()

















