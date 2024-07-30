from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Item, Address, CartItem, Cart, Cancel, Help, RequestItem, Account, SellProducts,Notice
from .forms import AddressForm, CancelForm, HelpForm, RequestItemForm, AccountForm, SellProductsForm
from django.contrib import messages
from plyer import notification
import time
from django.http import JsonResponse


# Create your views here.

# VIEW FOR USERS TO ACCESS HOMEPAGE OF SHOP
@login_required
def home_page(request):
    data = Item.objects.all()

    # Get search query
    search = request.GET.get('search')
    if search:
        data = data.filter(title__icontains=search)

    # Get filter parameters
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    category = request.GET.get('category')

    # Apply filters
    if min_price:
        data = data.filter(price__gte=min_price)
    if max_price:
        data = data.filter(price__lte=max_price)
    if category:
        data = data.filter(category__name__icontains=category)

    return render(request, 'ecom/home_page.html', {'data': data})


@login_required
def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category).exclude(pk=pk)  # Fetch related items
    return render(request, 'ecom/item_detail.html', {'item': item, 'related_items': related_items})


@login_required
def address(request, item_id):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user

            item = get_object_or_404(Item, id=item_id)
            address.item = item

            address.save()
            messages.success(request, f'Order placed for {address.item.title} successfully')
            return redirect('home_page')
    else:
        form = AddressForm()

    return render(request, 'ecom/address.html', {'form': form})


@login_required
def orders(request):
    orders = Address.objects.filter(user=request.user)
    search = request.GET.get('search')
    if search != None:
        orders = Address.objects.filter(user=request.user, status__icontains=search)
    return render(request, 'ecom/orders.html', {'orders': orders})


@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)

    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'{item} added to cart')
        notification.notify(
            title='VaultMe ecommerce solutions',
            message=f'{item} added to cart you can check your cart to view {item}'
        )
    return redirect('home_page')


@login_required
def cart_view(request):
    cart = Cart.objects.filter(user=request.user).first()
    total_price = 0
    if cart:
        items = cart.items.all()
        # Calculate the total price
        total_price = sum(item.item.price * item.quantity for item in items)
    else:
        items = []
    return render(request, 'ecom/cart.html', {'cart': cart, 'items': items, 'total_price': total_price})


@login_required
def remove_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
    cart_item.delete()
    messages.success(request, f'{cart_item.item.title} removed from your cart')
    return redirect('cart_view')


# CHECKOUT VIEW
# coming soon

@login_required
def coming_soon(request):
    return render(request, 'ecom/coming_soon.html')


# cancel order

@login_required
def cancel(request, pk):
    if request.method == 'POST':
        form = CancelForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.address = address
            item = get_object_or_404(Address, pk=pk, user=request.user)
            item.save()
            item.delete()
            messages.success(request, f'{item} cancellation request has been raised')
            time.sleep(3)
            notification.notify(
                title='VaultMe Ecommerce solutions',
                message=f'{item} cancelled successfully and your feedback was submitted\n Thank you {request.user} for using our services\n have a great day ahead!',
                timeout=8
            )
            return redirect('orders')
    else:
        form = CancelForm()

    return render(request, 'ecom/cancel.html', {'form': form})


# Change address
@login_required
def change_address(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, f'Address updated successfully for {address.item}')
            notification.notify(
                title='VaultMe ecommerce solutions',
                message=f'Address has been updated for your order {address.item}',
                timeout=5
            )
            return redirect('orders')
    else:
        form = AddressForm(instance=address)
    return render(request, 'ecom/change_address.html', {'form': form, 'address': address})


# function to raise help request
@login_required
def raise_help(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)  # Fetch the Address object
    if request.method == 'POST':
        form = HelpForm(request.POST, request.FILES)
        if form.is_valid():
            help = form.save(commit=False)
            help.user = request.user
            help.address = address  # Associate the address with the help request

            # Assuming 'item' is the required field in Help that needs to be set
            help.item = address.item  # Set the item or related object

            help.save()
            messages.success(request, f'Successfully raised help request for {help.item}')
            notification.notify(
                title='VaultMe ecommerce solutions',
                message=f'Help request raised for your order {help.item}\nOur team will reach you shortly!\nThank you {help.user} for your patience\nHave a great day ahead',
                timeout=5
            )
            return redirect('orders')
    else:
        form = HelpForm()
    return render(request, 'ecom/help.html', {'form': form})


@login_required
def request_item(request):
    if request.method == 'POST':
        form = RequestItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            messages.success(request, f'{item.item_name} requested successfully')
            notification.notify(
                title='VaultMe ecommerce solutions',
                message=f'hello {item.user}\n your request for {item.item_name} accepted successfully',
                timeout=8
            )
            return redirect('home_page')
    else:
        form = RequestItemForm()
    return render(request, 'ecom/request.html', {'form': form})


# SELLERS PAGE

@login_required
def seller_page(request):
    return render(request, 'ecom/seller_page.html')


# agreement
@login_required
def agreement(request):
    return render(request, 'ecom/agreement.html')


# set up account
@login_required
def set_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                account = form.save(commit=False)
                account.user = request.user
                account.save()
            except Exception as e:
                return JsonResponse({'message': str(e)}, status=400)
            messages.success(request, 'Account created successful')
            time.sleep(3)
            notification.notify(
                title='VaultMe Ecommerce solutions',
                message=f"Congratulations {account.user} your seller account has been created successfully\n you will "
                        f"receive your id card soon\n Welcome to VaultMe family",
                timeout=10

            )
            return redirect('set_account')
    else:
        form = AccountForm()
    return render(request, 'ecom/set_account.html', {'form': form})


# create view account

@login_required
def view_account(request):
    data = Account.objects.filter(user=request.user)
    return render(request, 'ecom/view_account.html', {'data': data})


# edit account

@login_required
def edit_account(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AccountForm(request.POST, request.FILES, instance=account)
        if form.is_valid():
            account.user = request.user
            form.save()
            messages.success(request, f'{account.user} your account has been updated!')
            return redirect('view_account')
    else:
        form = AccountForm(instance=account)
    return render(request, 'ecom/edit_account.html', {'form': form, 'account': account})


# sell products
@login_required
def sell_products(request):
    if request.method == 'POST':
        form = SellProductsForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            messages.success(request, f'{product.product_name} has been listed')
            return redirect('sell_products')
    else:
        form = SellProductsForm()
    data = SellProducts.objects.filter(user=request.user)
    return render(request, 'ecom/sell_products.html', {'form': form, 'data': data})


# delete product

@login_required
def delete_products(request, pk):
    product = get_object_or_404(SellProducts, pk=pk, user=request.user)
    product.delete()
    messages.success(request, f'{product.product_name} has been unlisted!')
    return redirect('sell_products')


# update product

@login_required
def update_product(request, pk):
    product = get_object_or_404(SellProducts, pk=pk, user=request.user)
    form = SellProductsForm(request.POST, request.FILES, instance=product)
    if form.is_valid():
        form.save()
        messages.success(request, f'{product.product_name} upgraded successfully')
        return redirect('sell_products')
    else:
        form = SellProductsForm(instance=product)
    return render(request, 'ecom/update_product.html', {'form': form, 'product': product})


# notice display

@login_required
def notices(request):
    data=Notice.objects.all()
    return render(request,'ecom/notices.html',{'data':data})












