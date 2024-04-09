from django.shortcuts import render,redirect
from .models import Order,OrderedItem
from product.models import Product
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse


def show_cart(request):
    try:
        user = request.user
        customer = user.customer_profile
        cart_obj, created = Order.objects.get_or_create(owner=customer, order_status=Order.CART_STAGE)
    except ObjectDoesNotExist:
        # Handle the case where customer_profile does not exist for the current user
        cart_obj = None

    context = {'cart': cart_obj}
    return render(request, 'cart.html', context)


def remove_item_from_cart(request,pk):
     item=OrderedItem.objects.get(pk=pk)
     if item:
        item.delete()
        return redirect('cart')
    

def checkout_cart(request):
    if request.method == 'POST':
        try:
            user = request.user
            customer = user.customer_profile
            total = float(request.POST.get('total'))
            order_obj = Order.objects.get(owner=customer, order_status=Order.CART_STAGE)

            if order_obj:
                order_obj.order_status = Order.ORDER_CONFIRMED
                order_obj.total_price = total
                order_obj.save()  

                status_message = "Your order is processed. Your items will be delivered within two days."
                messages.success(request, status_message)
        
        except Exception as e:
            status_message = "Something went wrong."
            messages.error(request, status_message)
            
        return redirect('cart')
    else:
        # Handle GET request here if needed
        pass


@login_required(login_url='account')
def add_to_cart(request):
    if request.method == 'POST':
        try:
            user = request.user
            customer = user.customer_profile
            quantity = int(request.POST.get('quantity'))
            product_id = request.POST.get('product_id')
            cart_obj, created = Order.objects.get_or_create(owner=customer, order_status=Order.CART_STAGE)
            product = Product.objects.get(pk=product_id)
            ordered_item, created = OrderedItem.objects.get_or_create(product=product, owner=cart_obj)

            if created:
                ordered_item.quantity = quantity
            else:
                ordered_item.quantity += quantity

            ordered_item.save()
            return redirect('cart')

        except ObjectDoesNotExist:
            # Handle the case where customer_profile does not exist for the current user
            return HttpResponse("User has no customer_profile. Please create a profile to continue.")

    else:
        return HttpResponse("Invalid request method. Only POST requests are allowed for this view.")

  
@login_required(login_url='account')
def show_orders(request):
    try:
        user = request.user
        customer = user.customer_profile
        all_orders = Order.objects.filter(owner=customer).exclude(order_status=Order.CART_STAGE)
    except ObjectDoesNotExist:
        # Handle the case where customer_profile does not exist for the current user
        all_orders = []

    context = {'orders': all_orders}
    return render(request, 'orders.html', context)
