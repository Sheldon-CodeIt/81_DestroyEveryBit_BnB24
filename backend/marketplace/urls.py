from django.urls import path
from .views import product_list, product_detail, add_to_cart, view_cart, delete_cart_item, add_comment, add_rating


urlpatterns = [
    path('', product_list, name='product_list'),
    path('<int:product_id>/', product_detail, name='api_product_detail'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='api_add_to_cart'),
    path('view-cart/', view_cart, name='api_view_cart'),
    path('delete-cart-item/<int:cart_item_id>/', delete_cart_item, name='api_delete_cart_item'),
    path('add-comment/<int:product_id>/', add_comment, name='api_add_comment'),
    path('add-rating/<int:product_id>/', add_rating, name='api_add_rating'),
]


