from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, CartItem, Comment, Rating
from django.views.decorators.csrf import csrf_exempt
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
    




@csrf_exempt
@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        try:
            product = Product.objects.get(pk=product_id)
            cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
            if not created:
                cart_item.quantity += 1
                cart_item.save()
            return JsonResponse({'message': f"{product.title} added to cart."})
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    cart_items_data = [{
        'product_id': item.product.pk,
        'title': item.product.title,
        'quantity': item.quantity,
        'price': item.product.price
    } for item in cart_items]
    return JsonResponse({'cart_items': cart_items_data, 'total_price': total_price})


@csrf_exempt
@login_required
def delete_cart_item(request, product_id):
    try:
        cart_item = CartItem.objects.get(user=request.user, product_id=product_id)
        cart_item.delete()
        return JsonResponse({'message': 'Item removed from cart.'})
    except CartItem.DoesNotExist:
        return JsonResponse({'error': 'Cart item not found.'}, status=404)


@login_required
def add_comment(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        text = request.POST.get('text')
        if text:
            Comment.objects.create(user=request.user, product=product, text=text)
            return JsonResponse({'message': 'Comment added successfully.'})
        else:
            return JsonResponse({'error': 'Comment cannot be empty.'}, status=400)
    return JsonResponse({'error': 'Method not allowed.'}, status=405)

@login_required
def add_rating(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        rating = request.POST.get('rating')
        if rating:
            Rating.objects.create(user=request.user, product=product, rating=rating)
            return JsonResponse({'message': 'Rating added successfully.'})
        else:
            return JsonResponse({'error': 'Rating cannot be empty.'}, status=400)
    return JsonResponse({'error': 'Method not allowed.'}, status=405)



