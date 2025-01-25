from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Tax(models.Model):
    tax_name = models.CharField(max_length=20)
    tax_percentage = models.FloatField()

    def __str__(self):
        return '{}  {} %'.format(str(self.tax_name),(self.tax_percentage))
    
class AddOns(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0)
    status = models.BooleanField(default=True)



class FoodCategory(models.Model):
    name = models.CharField(max_length=20)
    image = models.FileField(upload_to='category_images')
    date_added = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)


class Menu(models.Model):
    category = models.ForeignKey('FoodCategory', on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=255)
    image = models.FileField(upload_to='foodimage')
    options = (("Quarter", "Quarter"), ("Half", "Half"), ("Full", "Full"))
    options2 = (("Small", "Small"), ("Medium", "Medium"), ("Large", "Large"))
    potion = models.CharField(max_length=255, choices=options2)  # Fixed typo from potion to portion
    options1 = (("Veg", "Veg"), ("Non-Veg", "Non-Veg"), ("Egg", "Egg"))
    diet = models.CharField(max_length=20, choices=options1)
    price = models.FloatField()
    status = models.BooleanField(default=True)
    stock = models.IntegerField()
    description = models.CharField(max_length=1000, null=True, blank=True)
    create_date = models.DateField(auto_now_add=True)
    # Code of product for searching

    code = models.CharField(max_length=10, null=True, unique=True)

    # Additional fields
    price_Before_tax = models.FloatField(null=True, blank=True)
    tax_amount = models.FloatField(null=True, blank=True)

    # Tax calculation
    tax = models.CharField(max_length=20, choices=(("Inclusive", "Inclusive"), ("Exclusive", "Exclusive")))
    tax_value = models.ForeignKey(Tax, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.price is not None:
            self.price = float(self.price)  # Ensure self.price is a float
            if self.tax_value:
                tax_rate = self.tax_value.tax_percentage / 100
                if self.tax == "Exclusive":
                    self.tax_amount = round(self.price * tax_rate, 2)
                    self.price_Before_tax = round(self.price, 2)
                    self.price = round(self.price + self.tax_amount, 2)
                elif self.tax == "Inclusive":
                    self.price_Before_tax = round(self.price / (1 + tax_rate), 2)
                    self.tax_amount = round(self.price - self.price_Before_tax, 2)
            else:
                self.price_Before_tax = round(self.price, 2)
                self.tax_amount = 0.0
        else:
            self.price_Before_tax = 0.0
            self.tax_amount = 0.0

        super(Menu, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Tables(models.Model):
    Table_number = models.IntegerField()
    Number_of_Seats = models.IntegerField()
    date_added = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        if self.Table_number == 100:
            return "Takeaway"
        return f"Table: {self.Table_number}"


class Order(models.Model):

    token = models.IntegerField(default=0)
    table = models.ForeignKey(Tables, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming you have a user model for waiters/chefs
    create_date = models.DateTimeField(auto_now_add=True)
    status_options = (("In Kitchen","In Kitchen"),("Pending", "Pending"), ("In Progress", "In Progress"),("Order Ready","Order Ready"), ("Completed", "Completed"))
    status = models.CharField(max_length=20, choices=status_options, default="Pending")
    checkout_status = models.BooleanField(default=False)
    take_order = models.BooleanField(default=False)
    vehicle_number = models.CharField(max_length=20, null=True, blank=True)
    completion_status = models.BooleanField(default=False)

    total_price = models.FloatField(default=0)
    total_tax = models.FloatField(default=0)
    total_before_tax = models.FloatField(default=0)
    payment_method = models.CharField(max_length=50, default="Pending")
    payment_status = models.CharField(max_length=20, choices=(("Pending", "Pending"), ("Paid", "Paid")),default="Pending")

    def save(self, *args, **kwargs):
        if not self.pk:
            today = now().date()
            last_token = Order.objects.filter(create_date__date=today).aggregate(
                max_token=models.Max('token')
            )['max_token'] or 0
            self.token = last_token + 1  # Increment the token
            print(f"Generated token: {self.token}")  # Debugging print

        super().save(*args, **kwargs)
    

    def __str__(self):
        return f"#{self.id} -  {self.table}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.FloatField()
    special_instructions = models.CharField(max_length=500, null=True, blank=True)
    add_ons = models.ManyToManyField(AddOns,null=True, blank=True)
    completion_status = models.BooleanField(default=False) 

    def save(self, *args, **kwargs):
        self.price = round(self.price, 2)
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"

    def get_total_price(self):
        return self.quantity * self.price
    

class Checkout(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    total_price = models.FloatField()
    tax_amount = models.FloatField(null = True, blank=True)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20, choices=(("Pending", "Pending"), ("Paid", "Paid")))
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Checkout for Order {self.order.id}"
    

class RestaurantDetails(models.Model):
    Name_of_restaurant = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    TRN = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    Address = models.TextField(null=True, blank=True)
    logo = models.FileField(upload_to="logo", null=True, blank=True)


    def __str__(self):
        return str(self.Name_of_restaurant)