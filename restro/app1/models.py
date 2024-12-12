from django.db import models
from django.db import models
#from app1 import views


# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length = 100)
    email = models.EmailField()
    mobile = models.BigIntegerField()
    password = models.CharField(max_length =100)

class Product(models. Model):
    CAT =(( 'VEG DISHES',1),('NON-VEG DISHES',2),('VEG STARTUP',3),('NON_VEJ STARTUP',4),('DESSERT',5),('COLD-DRINKS',6),('CHINESE',7))
    name = models.CharField(max_length = 50, verbose_name = "Product Name")
    price = models.IntegerField()
    cat = models.CharField(max_length = 50, verbose_name = "Category", choices = CAT)
    pdetails = models.CharField(max_length = 1000, verbose_name = "Product Details")
    is_active = models.BooleanField(default = True)
    pimage = models.ImageField(upload_to='static/image')

    def __str__(self):
       return self.name

class Cart(models.Model):
   user_id = models.ForeignKey('auth.user', on_delete = models.CASCADE, db_column ='user_id')
   pid = models.ForeignKey('Product', on_delete = models.CASCADE, db_column = "pid")
   qty = models.IntegerField(default = 1)

class Order(models.Model):
    order_id = models.CharField(max_length=50)
    user_id = models.ForeignKey('auth.user', on_delete = models.CASCADE, db_column ='user_id')
    pid = models.ForeignKey('Product', on_delete = models.CASCADE,db_column = "pid")
    qty = models.IntegerField(default = 1)
    amt = models.FloatField()





