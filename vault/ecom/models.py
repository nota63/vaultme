from datetime import timezone

from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.utils import timezone
from tinymce.models import HTMLField


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)  # The name of the category

    # slug = models.SlugField(unique=True)  # A unique identifier for the category, used in URLs

    def __str__(self):
        return self.name


class Item(models.Model):
    title = models.CharField(max_length=255)  # The name of the item
    description = models.TextField()  # A detailed description of the item
    price = models.DecimalField(max_digits=10, decimal_places=2)  # The price of the item
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True,
                                         null=True)  # Optional discounted price
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)  # Link to the category
    image = models.ImageField(upload_to='items/', blank=True, null=True)  # Optional image for the item
    # slug = models.SlugField(unique=True)  # A unique identifier for the item, used in URLs
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the item was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when the item was last updated
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who posted the item

    def __str__(self):
        return self.title  # This will return the title of the item when we print it

    def get_discounted_price(self):
        if self.discount_price:
            return self.discount_price  # If there's a discount price, return it
        return self.price  # Otherwise, return the regular price


# buy address
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    contact = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=10000)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100,
                               choices=(('India', 'India'), ('Africa', 'Africa'), ('US', 'US'), ('Dubai', 'Dubai')))
    placed_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=100, null=True, blank=True, choices=(
        ('shipped', 'shipped'), ('on the way', 'on the way'), ('out for delivery', 'out for delivery'),
        ('near to you', 'near to you'), ('order confirmed', 'order confirmed'), ('delivered', 'delivered'),
        ('could not deliver!', 'could not deliver'), ('waiting for seller to proceed', 'waiting for seller to proceed'),
        ('will be deliver shortly', 'will be deliver shortly')), default=('Order confirmed'))
    custom_status = models.CharField(max_length=2000, null=True, blank=True,
                                     default=('Delivery date will be available soon.'))
    expected_delivery_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Order from {self.user} for {self.item}"


# create models to handle help requests

class Help(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    type = models.CharField(max_length=500, choices=(
        ('Fast delivery', 'Fast delivery'), ('deliver on my given time', 'deliver on my given time'),
        ('read my message', 'read my message')))
    message = models.CharField(max_length=50000)
    attach_image = models.ImageField(upload_to='help_request_images/')
    email = models.EmailField(null=True, blank=True)
    contact = models.CharField(max_length=20, null=True, blank=True)
    raised_on = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"Help request from {self.user} for {self.item}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"


# cancel

class Cancel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    why_cancel = models.CharField(max_length=1000, choices=(('The item is too expensive', 'The item is too expensive'),
                                                            ('found better deal somewhere',
                                                             'found better deal somewhere')))
    suggestion = models.CharField(max_length=1000)

    def __str__(self):
        return f"User {self.user} Cancelled {self.item}"


# create request an item form

class RequestItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=500)
    description = models.CharField(max_length=600)
    image = models.ImageField(upload_to='requestItems/')
    contact = models.CharField(max_length=15)
    requested_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Item requested by {self.user}"


# create model to set up bank and seller account

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='sellers/')
    bank_account = models.CharField(max_length=500)
    bank_name = models.CharField(max_length=500)
    ifsc_code = models.CharField(max_length=300)
    email = models.EmailField()
    city = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=500)
    date_created = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f" Seller Account of {self.user}"


# create model to sell products
class SellProducts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    product_pdf = models.FileField(upload_to='sellerProducts/')
    price = models.CharField(max_length=1000)
    status = models.CharField(max_length=200, choices=(
    ('Accepted', 'Accepted'), ('Rejected', 'Rejected'), ('Pending', 'Pending'), ('Coming to pick', 'Coming to pick')),
                              default=('Pending'), null=True, blank=True)
    message = models.CharField(max_length=1000, null=True, blank=True)
    date_listed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Product sell request from {self.user} for {self.product_name}"


# create model to notice board
class Notice(models.Model):
    title = models.CharField(max_length=100)
    content = HTMLField()
    attachment_pdf = models.FileField(upload_to='attachments/')
    date_posted=models.DateTimeField(auto_now=True,null=True, blank=True)



