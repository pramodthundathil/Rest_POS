from django.db import models
from django.contrib.auth.models import User

class FoodCategory(models.Model):
    name = models.CharField(max_length=20)
    image = models.FileField(upload_to='category_images')
    date_added = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)


class Menu(models.Model):
    category = models.ForeignKey(FoodCategory,on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255)
    image = models.FileField(upload_to='foodimage')
    options = (("Quarter","Quarter"),("Half","Half"),("Full","Full"))
    potion = models.CharField(max_length=255,choices=options)
    options1 = (("Veg","Veg"),("Non-Veg","Non-Veg"),("Egg","Egg"))
    diet = models.CharField(max_length=20,choices=options1)
    price = models.FloatField()
    status = models.BooleanField(default=True)
    stock = models.IntegerField()
    description = models.CharField(max_length=1000, null=True, blank=True)
    create_date = models.DateField(auto_now_add=True)

class Tables(models.Model):
    Table_number = models.IntegerField()
    Number_of_Seats = models.IntegerField()
    date_added = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(f"Table: {self.Table_number}")


class Order(models.Model):

    table = models.ForeignKey(Tables, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming you have a user model for waiters/chefs
    create_date = models.DateTimeField(auto_now_add=True)
    status_options = (("In Kitchen","In Kitchen"),("Pending", "Pending"), ("In Progress", "In Progress"),("Order Ready","Order Ready"), ("Completed", "Completed"))
    status = models.CharField(max_length=20, choices=status_options, default="Pending")
    checkout_status = models.BooleanField(default=False)
    take_order = models.BooleanField(default=False)
    completion_status = models.BooleanField(default=False)

    def __str__(self):
        return f"#{self.id} - Table {self.table.Table_number}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.FloatField()
    special_instructions = models.CharField(max_length=500, null=True, blank=True)
    completion_status = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"

    def get_total_price(self):
        return self.quantity * self.price
    

class Checkout(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    total_price = models.FloatField()
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20, choices=(("Pending", "Pending"), ("Paid", "Paid")))
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Checkout for Order {self.order.id}"