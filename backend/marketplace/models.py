from django.db import models
from django.contrib.auth.models import User
from brand.models import BrandProfile


class Product(models.Model):
    product_id = models.CharField(max_length=100, primary_key=True)  # Setting product_id as primary key
    brand = models.ForeignKey(BrandProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    sustainability = models.CharField(max_length=100)
    ingredients = models.TextField()
    certification = models.CharField(max_length=100)
    recycling_category = models.CharField(max_length=100)
    origin = models.CharField(max_length=100)
    labor_practices = models.TextField()
    environmental_footprint = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.product.title}"

class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()

    def __str__(self):
        return f"Rating {self.rating} for {self.product.title}"
    


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.title} ({self.user.username})"




    
