from django.db import models

# Create your models here.

class Contact(models.Model):
    yourName = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.yourName


class Destination(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default = 50000)
    days = models.IntegerField(default=1)
    desc = models.TextField()
    offer = models.BooleanField(default=False)
    img1=models.ImageField(upload_to='pics')
    img2 = models.ImageField(upload_to='pics')
    img3 = models.ImageField(upload_to='pics')
    day1= models.CharField(max_length=200, blank=True, null=True)
    day2 = models.CharField(max_length=200, blank=True, null=True)
    day3 = models.CharField(max_length=200, blank=True, null=True)
    day4 = models.CharField(max_length=200, blank=True, null=True)
    day5 = models.CharField(max_length=200, blank=True, null=True)
    day6 = models.CharField(max_length=200, blank=True, null=True)
    day7 = models.CharField(max_length=200, blank=True, null=True)
    day8 = models.CharField(max_length=200, blank=True, null=True)
    day9 = models.CharField(max_length=200, blank=True, null=True)
    day10 = models.CharField(max_length=200, blank=True, null=True)
    day11 = models.CharField(max_length=200, blank=True, null=True)
    day12 = models.CharField(max_length=200, blank=True, null=True)
    day13 = models.CharField(max_length=200, blank=True, null=True)
    day14 = models.CharField(max_length=200, blank=True, null=True)
    day15 = models.CharField(max_length=200, blank=True, null=True)
    day16 = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

class ConfirmBooking(models.Model):
    fullName = models.CharField(max_length=200,default="")
    fromCity = models.CharField(max_length=100)
    toCity = models.CharField(max_length=100)
    depatureDate = models.DateField()
    days = models.IntegerField(default=1)
    noOfRooms = models.IntegerField()
    noOfAdults = models.IntegerField()
    noOfChildren = models.IntegerField()
    email = models.EmailField(max_length=254)
    phoneNo = models.CharField(max_length=12)
    amountPerPerson = models.IntegerField(default=0)
    totalAmount = models.FloatField(default=0)
    userName = models.CharField(max_length=200, default="")
    date = models.DateField(("Date"), auto_now_add=True)


    def __str__(self):
        return self.fullName
