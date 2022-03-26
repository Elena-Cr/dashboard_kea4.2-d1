# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Customers(models.Model):
    customer_id = models.BigIntegerField(primary_key=True)
    first_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    postcode = models.BigIntegerField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    ascii_safe_email = models.TextField(blank=True, null=True)
    date_of_birth = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customers'
   
    def __str__(self):
        return str(self.customer_id) + ' - ' + self.first_name + ' ' + self.last_name + ' - ' + self.country
    


class Employees(models.Model):
    employee_id = models.BigIntegerField(primary_key=True)
    firstname = models.TextField(blank=True, null=True)
    lastname = models.TextField(blank=True, null=True)
    date_of_birth = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employees'

    def __str__(self):
        return str(self.employee_id) + ' - ' + self.firstname + ' ' + self.lastname + ' - ' + str(self.date_of_birth)
    

class Geodata(models.Model):
    index = models.BigIntegerField(primary_key=True)
    country = models.TextField(blank=True, null=True)
    lat = models.TextField(blank=True, null=True)
    lon = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'geodata'

    def __str__(self):
        return str(self.index) + ' - ' + self.country


class Orders(models.Model):
    index = models.BigIntegerField(primary_key=True)
    order_id = models.BigIntegerField(blank=True, null=True)
    product_id = models.BigIntegerField(blank=True, null=True)
    unitprice = models.FloatField(blank=True, null=True)
    quantity = models.BigIntegerField(blank=True, null=True)
    customer_id = models.BigIntegerField(blank=True, null=True)
    orderdate = models.DateTimeField(blank=True, null=True)
    employee_id = models.BigIntegerField(blank=True, null=True)
    deliverydate = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'
    
    def __str__(self):
        return str(self.index) + ' - ' + str(self.order_id) + ' - Sale Value: ' + str(round(self.unitprice * self.unitprice, 2))


class Products(models.Model):
    product_id = models.BigIntegerField(primary_key=True)
    productname = models.TextField(blank=True, null=True)
    stock = models.BigIntegerField(blank=True, null=True)
    reorder = models.BigIntegerField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products'
    
    def __str__(self):
        return str(self.product_id) + ' - ' + self.productname + ' (' + self.type + ') - Stock: ' + str(self.stock)
