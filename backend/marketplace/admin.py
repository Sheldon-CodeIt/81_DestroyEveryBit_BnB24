from django.contrib import admin
from .models import Product, Comment, Rating, CartItem


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'price', 'created_at')  # Customize the fields displayed in the admin list view
    search_fields = ('title', 'brand__brand_name')  # Enable searching by title and brand name
    list_filter = ('brand__brand_name',)  # Add filter by brand name

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')  # Customize the fields displayed in the admin list view
    search_fields = ('user__username', 'product__title')  # Enable searching by username and product title
    list_filter = ('product__title',)  # Add filter by product title

class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'get_created_at')  # Customize the fields displayed in the admin list view
    search_fields = ('user__username', 'product__title')  # Enable searching by username and product title
    list_filter = ('product__title',)  # Add filter by product title
    
    def get_created_at(self, obj):
        return obj.created_at
    get_created_at.admin_order_field = 'created_at'
    get_created_at.short_description = 'Created At'

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity')  # Customize the fields displayed in the admin list view
    search_fields = ('user__username', 'product__title')  # Enable searching by username and product title
    list_filter = ('product__title',)  # Add filter by product title

# Register the models with their custom admin classes
admin.site.register(Product, ProductAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Rating, RatingAdmin)
# Register the CartItem model with its custom admin class
admin.site.register(CartItem, CartItemAdmin)