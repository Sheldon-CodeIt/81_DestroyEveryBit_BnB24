from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, CartItem, Comment, Rating
from django.contrib import messages



def product_list(request):
    products = Product.objects.all()
    product_data = [{'product_id': product.pk, 'title': product.title, 'description': product.description, 'price': product.price} for product in products]
    return JsonResponse(product_data, safe=False)


def product_detail(request, product_id):
    try:
        product = Product.objects.get(product_id=product_id)  # Use product_id instead of id
        product_json = {
            'product_id': product.product_id,
            'title': product.title,
            'description': product.description,
            'price': product.price,
            'image': product.image.url,
            'sustainability': product.sustainability,
            'ingredients': product.ingredients,
            'certification': product.certification,
            'recycling_category': product.recycling_category
        }
        return JsonResponse(product_json)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    
@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{product.title} added to cart.")
    return redirect('product_list')

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'marketplace/cart.html', {'cart_items': cart_items, 'total_price': total_price})




@login_required
def delete_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('view_cart')

@login_required
def add_comment(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        text = request.POST.get('text')
        if text:
            Comment.objects.create(user=request.user, product=product, text=text)
            messages.success(request, "Comment added successfully.")
        else:
            messages.error(request, "Comment cannot be empty.")
    return redirect('product_detail', product_id=product_id)

@login_required
def add_rating(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        rating = request.POST.get('rating')
        if rating:
            Rating.objects.create(user=request.user, product=product, rating=rating)
            messages.success(request, "Rating added successfully.")
        else:
            messages.error(request, "Rating cannot be empty.")
    return redirect('product_detail', product_id=product_id)


