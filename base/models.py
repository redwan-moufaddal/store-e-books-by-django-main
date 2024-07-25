from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django_resized import ResizedImageField
from django.utils.html import format_html
from All_users.models import User



CATEGORY_CHOICES = [
    ('Arts & Photography', 'Arts & Photography'),
    ('Biographies', 'Biographies'),
    ('Business & Money', 'Business & Money'),
    ('Calendars', 'Calendars'),
    ('Children\'s Books', "Children's Books"),
    ('Comics', 'Comics'),
    ('Performance Filters', 'Performance Filters'),
    ('Cookbooks', 'Cookbooks'),
    ('Accessories', 'Accessories'),
    ('Education', 'Education'),
    ('Indoor Living', 'Indoor Living'),
]



class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    author = models.CharField(max_length=50)
    price_new = models.DecimalField(max_digits=10, decimal_places=2)
    price_old = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_percentage = models.IntegerField(null=True, blank=True)
    category = models.CharField(max_length=25, choices=CATEGORY_CHOICES)
    reviews = models.IntegerField(null=True, blank=True)
    pid = ShortUUIDField(unique=True, length=10, max_length=30, prefix="prod", alphabet="abcdefgh12345", null=True, blank=True)
    first_image = ResizedImageField(help_text=format_html('<h5 style="color:red;"><b>The first interface (size: 700x700px)</b></h5>'),size=[700, 700], crop=['top', 'left'], upload_to='image/')
    second_image = ResizedImageField(help_text='<h5 style="color:red;"><b>The second interface (size: 700x700px)</b></h5>',size=[700, 700], crop=['top', 'left'], upload_to='image/')
    upload_book = models.FileField(upload_to='book', null=True, blank=True)





    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.price_old is not None and self.price_old != 0:
            self.discount_percentage = ((self.price_old - self.price_new) / self.price_old) * 100
        else:
            # Handle the case where price_old is None or 0 to avoid division by zero
            self.discount_percentage = 0
        super().save(*args, **kwargs)
    def get_category_display_name(self):
        # Function to get the user-friendly display name
        return dict(self.CATEGORY_CHOICES).get(self.category, 'Unknown Category')

    def __str__(self):
        return str(self.name)




class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField(max_length=450)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=150)
    rate = models.IntegerField(default=0)
    userid = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} date:{self.created}"




class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
