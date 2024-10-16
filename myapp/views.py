from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import *
from .forms import *
import logging
import re
import razorpay
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate,login as usrlogin,logout as usrlogout
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest



# @login_required(login_url='login/')
def index(r):
    books = addproduct.objects.all().order_by('-id')[:15]
    totalitem = 0
    wishitem = 0
    if r.user.is_authenticated:
        totalitem = cartpro.objects.filter(user=r.user).count()
        wishitem = wishlist.objects.filter(user=r.user).count()
    search = r.GET.get('srch')
    print("search query:", search)
    if search:
        books = addproduct.objects.filter(pnm__icontains=search)
    else:
        books = addproduct.objects.all()

    context = {
        'CATEGORY_CHOICES': addproduct.CATEGORY_CHOICES,
        'search':search,
        'totalitem': totalitem,
        'wishitem': wishitem,
        'books':books
    }

    return render(r, 'base.html', context)

@login_required(login_url='login/')
def admin_index(r):
    total_pendings = orderplaced.objects.filter(status='Pending').count()
    completed_payments = payment.objects.filter(paid=True).count()
    orders_placed = orderplaced.objects.count()
    products_added = addproduct.objects.count()
    normal_users = User.objects.filter(is_superuser=False).count()
    admin_users = User.objects.filter(is_superuser=True).count()
    total_users = User.objects.count()
    total_messages = ContactMessage.objects.count()

    context = {
        'total_pendings': total_pendings,
        'completed_payments': completed_payments,
        'orders_placed': orders_placed,
        'products_added': products_added,
        'normal_users': normal_users,
        'admin_users': admin_users,
        'total_users': total_users,
        'total_messages':total_messages,
    }

    return render(r, 'adminboard.html', context)


def register(r):
    obj = regform()
    if r.method == 'POST':
        fname = r.POST.get('firstname')
        ln = r.POST.get('lastname')
        un = r.POST.get('username')
        p1 = r.POST.get('psw')
        p2 = r.POST.get('cpsw')
        em = r.POST.get('email')
        
        if p1 != p2:
            messages.error(r, 'Password and Confirm Password do not match!')
            return redirect(register)
        
        if User.objects.filter(username=un).exists():
            messages.error(r, 'Username already exists. Try another one.')
            return redirect(register)
        
         # Validate email format
        try:
            validate_email(em)
        except ValidationError:
            messages.error(r, 'Please enter a valid email address.')
            return redirect(register)

        if User.objects.filter(email=em).exists():
            messages.error(r, 'Email already registered. Try logging in.')
            return redirect(register)
        
         # Validate password strength
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', p1):
            messages.error(r, 'Password must be at least 8 characters long and include at least one uppercase letter, one lowercase letter, one number, and one special character.')
            return redirect(register)

        usr = User.objects.create_user(username=un, password=p1, first_name=fname, last_name=ln, email=em)
        usr.save()
        
        messages.success(r, 'Successfully registered! Please log in.')
        # return redirect('login')
    
    return render(r, 'register.html', {'form': obj})

def login(r):
    if r.method=='POST':
        un=r.POST.get('un')
        pa=r.POST.get('pa')
        print("UN",un,"PWD",pa)
        remember_me = r.POST.get('remember_me')
        
        usr = authenticate(username=un, password=pa)
        print('usr',usr)
        if usr is not None:
            usrlogin(r, usr)

            # Remember Me
            if remember_me:
                r.session.set_expiry(1209600) 
            else:
                r.session.set_expiry(0)  


            if usr.is_superuser:
                return redirect('admin_index')  
            else:
                return redirect('index')
                
            
        else:
            messages.error(r, 'Invalid username or password')

            return render(r, 'base.html', {'un': un})
    
    return render(r, 'base.html')

@login_required
def changepwd(request):
    if request.method == 'POST':
        form = MyPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('pwdchangedone')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = MyPasswordChangeForm(request.user)
    return render(request, 'changepwd.html', {'form': form})

@login_required
def pwdchangedone(request):
    return render(request, 'passwordchangedone.html')


@login_required(login_url='login/')
def profile(r):
    form = CustomerProfileForm()
    if r.method=='POST':
        vform=CustomerProfileForm(r.POST)
        if vform.is_valid():
            user = r.user
            name = vform.cleaned_data['name']
            locality = vform.cleaned_data['locality']
            district = vform.cleaned_data['district']
            mobile = vform.cleaned_data['mobile']
            state = vform.cleaned_data['state']
            zipcode = vform.cleaned_data['zipcode']
            if customer.objects.filter(
                user=user,
                name=name,
                locality=locality,
                district=district,
                mobile=mobile,
                state=state,
                zipcode=zipcode
            ).exists():
                messages.warning(r, 'This address already exists.')
            else:
                reg = customer(
                    user=user,
                    name=name,
                    locality=locality,
                    mobile=mobile,
                    district=district,
                    state=state,
                    zipcode=zipcode
                )
                reg.save()
                messages.success(r,'Congratulations! Profile Save Successfully')
        else:
            messages.warning(r,'Invalid Input Data')
    return render(r,'profile.html',{'form':form})    

def address(r):
    add = customer.objects.filter(user=r.user)
    return render(r,'address.html',{'add':add})

def updateAddress(r,id):
    add = customer.objects.get(id=id)
    form = CustomerProfileForm(instance=add)
    if r.method=="POST":
        vform=CustomerProfileForm(r.POST,instance=add)
        if vform.is_valid():
            vform.save()
            return redirect(address)
    return render(r,'updateAddress.html',{'form':form})

def delete(r,id):
    user = r.user
    add = customer.objects.get(id=id)
    add.delete()
    return redirect(address)

@login_required(login_url='login/')
def addprod(r):
    user = r.user
    if r.method == 'POST':
        pnm = r.POST['name']
        athr = r.POST['author']
        cat = r.POST['cat']
        lang = r.POST['lang']
        publ = r.POST['publisher']
        isbn = r.POST['isbn']
        pr = r.POST['price']
        qty = r.POST['quantity']
        img = r.FILES.get('pimg')

        # Check if the product already exists
        if addproduct.objects.filter(pnm=pnm, athr=athr, cat=cat, lang=lang, publ=publ, isbn=isbn).exists():
            # Product already exists, show a message
            message = f"The product '{pnm}' by '{athr}' is already added."
            return render(r, 'addproduct.html', {
                'CATEGORY_CHOICES': addproduct.CATEGORY_CHOICES,
                'LANGUAGE_CHOICES': addproduct.LANGUAGE_CHOICES,
                'message': message
            })
        else:
            # Add the new product
            if img:
                sobj = addproduct(user=user, pnm=pnm, athr=athr, cat=cat, lang=lang, publ=publ, isbn=isbn, pr=pr, qty=qty, img=img)
                sobj.save()
                message = f"The product '{pnm}' by '{athr}' has been added successfully."
                return render(r, 'addproduct.html', {
                    'CATEGORY_CHOICES': addproduct.CATEGORY_CHOICES,
                    'LANGUAGE_CHOICES': addproduct.LANGUAGE_CHOICES,
                    'message': message
                })

    return render(r, 'addproduct.html', {
        'CATEGORY_CHOICES': addproduct.CATEGORY_CHOICES,
        'LANGUAGE_CHOICES': addproduct.LANGUAGE_CHOICES
    })


def prodisplay(r):
    user=r.user
    query = r.GET.get('search')
    if query:
        products = addproduct.objects.filter(pnm__icontains=query)
    else:
        products = addproduct.objects.all()
    
    return render(r,'prodisplay.html',{'products':products})


def editpro(r, id):
    # product = get_object_or_404(addproduct, id=id)
    products = addproduct.objects.filter(id=id).first()
    if r.method == 'POST':
        products.pnm = r.POST['name']
        products.athr = r.POST['author']
        products.cat = r.POST['cat']
        products.lang = r.POST['lang']
        products.publ = r.POST['publisher']
        products.isbn = r.POST['isbn']
        products.pr = r.POST['price']
        products.qty = r.POST['quantity']
        img = r.FILES.get('image')
        if img:
            products.img = img
        products.save()
        return redirect('prodisplay')

    return render(r, 'editproduct.html', {'products': products})

def remove(r,id):
    user = r.user
    products = addproduct.objects.get(id=id)
    products.delete()
    return redirect(prodisplay)

def admin_stock(r):
    products = addproduct.objects.all()
    return render(r,'adminstock.html',{'products':products})

def update_stock(request, product_id):
    product = get_object_or_404(addproduct, id=product_id)
    if request.method == 'POST':
        form = UpdateStockForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('adminstock')
    else:
        form = UpdateStockForm(instance=product)
    return render(request, 'update_stock.html', {'form': form, 'product': product})


def admin_orders(request):
    if request.method == "POST":
        order_id = request.POST.get('order_id')
        update_status = request.POST.get('update_status')  

        if order_id and update_status:
            order = get_object_or_404(orderplaced, id=order_id)
            order.status = update_status
            order.save()
            return redirect('adminorders')  

    status_choices = orderplaced._meta.get_field('status').choices
    orders = orderplaced.objects.select_related('user', 'Customer', 'product', 'Payment').all()
    return render(request, 'admin_orders.html', {'orders': orders, 'status_choices': status_choices})

def delete_order(r, order_id):
    order = orderplaced.objects.get(id=order_id)
    order.delete()
    return redirect('adminorders')

def admin_users(r):
    users = User.objects.all()
    return render(r, 'admin_users.html', {'users': users})

def delete_user(r, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('adminusers')

def admin_contact(r):
    messages = ContactMessage.objects.all()

    # status_choices = [("read", "Read"), ("unread", "Unread")]

    context = {
        'messages': messages,
        # 'status_choices': status_choices,
    }
    return render(r, 'admin_contacts.html', context)

def delete_message(r, id):
    message = get_object_or_404(ContactMessage, id=id)
    message.delete()
    return redirect('adminmessages')

def category_books(r, category):
    totalitem = 0
    wishitem = 0
    if r.user.is_authenticated:
        totalitem = cartpro.objects.filter(user=r.user).count()
        wishitem = wishlist.objects.filter(user=r.user).count()

    search = r.GET.get('srch')
    print("Search query:", search)
    if search:
        books = addproduct.objects.filter(cat=category, pnm__icontains=search)
    else:
        books = addproduct.objects.filter(cat=category)
    
    
    return render(r, 'category_list.html', {'books': books,'search':search,'selected_category': category,'CATEGORY_CHOICES': addproduct.CATEGORY_CHOICES,'totalitem':totalitem,'wishitem':wishitem})

def all_books(r):
    totalitem = 0
    wishitem = 0
    if r.user.is_authenticated:
        totalitem = cartpro.objects.filter(user=r.user).count()
        wishitem = wishlist.objects.filter(user=r.user).count()

    search = r.GET.get('srch')
    print("search query:", search)
    if search:
        books = addproduct.objects.filter(pnm__icontains=search)
    else:
        books = addproduct.objects.all()

    return render(r, 'all_books.html', {'books': books,'search':search,'CATEGORY_CHOICES': addproduct.CATEGORY_CHOICES,'totalitem':totalitem,'wishitem':wishitem})

def book_detail(r, book_id):
    totalitem = 0
    wishitem = 0
    if r.user.is_authenticated:
        totalitem = cartpro.objects.filter(user=r.user).count()
        wishitem = wishlist.objects.filter(user=r.user).count()
    book = get_object_or_404(addproduct, id=book_id)
    reviews = Review.objects.filter(book=book)
    user = r.user
    cart_products = cartpro.objects.filter(user=user).values_list('product', flat=True)
    wishlist_items = wishlist.objects.filter(user=user).values_list('product', flat=True)

    in_cart = book.id in cart_products
    in_wishlist = book.id in wishlist_items

    return render(r, 'book_detail.html', {
        'book': book,
        'reviews': reviews,
        'range_5': range(1, 6),
        'CATEGORY_CHOICES': addproduct.CATEGORY_CHOICES,
        'in_cart': in_cart,
        'in_wishlist': in_wishlist,
        'totalitem':totalitem,
        'wishitem':wishitem,
    })

def addtocart(r):
    user=r.user
    product_id=r.GET.get('prod_id')
    product=addproduct.objects.get(id=product_id)
    cartpro(user=user,product=product).save()
    return redirect(cart)
    

def cart(r):
    totalitem = 0
    wishitem = 0
    if r.user.is_authenticated:
        totalitem = cartpro.objects.filter(user=r.user).count()
        wishitem = wishlist.objects.filter(user=r.user).count()
    user = r.user
    cart_items = cartpro.objects.filter(user=user)
    cart = []
    amount = 0
    for item in cart_items:
        value = item.quantity * item.product.discounted_price()  
        cart.append({
            'product': item.product,
            'quantity': item.quantity,
            'value': value
        })
        amount = amount + value
    shipping_cost = 0 if amount > 500 else 70
    totalamount = amount + shipping_cost
    return render(r, 'cart.html', {'cart': cart,'CATEGORY_CHOICES': addproduct.CATEGORY_CHOICES, 'amount': amount,'shipping_cost':shipping_cost, 'totalamount': totalamount,'totalitem':totalitem,'wishitem':wishitem})

# def cart(r):
#     user=r.user
#     cart= cartpro.objects.filter(user=user)
#     amount=0
#     for item in cart:
#         item.value = item.quantity * item.product.discounted_price
#         amount = amount + item.value
#         totalamount = amount + 70
#     return render(r,'cart.html',{'cart': cart, 'amount': amount, 'totalamount': totalamount})

def cart_update(r,id):
    print('updating cart for product id:', id)
    user= r.user
    product = get_object_or_404(addproduct, id=id)
    cart_item = cartpro.objects.filter(user=user, product=product).first()
    # cart_item = cartpro.objects.filter(user=user, product_id=id).first()
    if cart_item:
        print(f"Current cart item quantity: {cart_item.quantity}")
        print(f"Current stock quantity: {product.qty}")
        if cart_item.quantity < product.qty:
            cart_item.quantity = cart_item.quantity + 1
            cart_item.save()
            product.qty = product.qty - 1  # Reduce stock quantity
            product.save()
            print(f"New cart item quantity: {cart_item.quantity}")
            print(f"New stock quantity: {product.qty}")
            messages.success(r, "Item quantity updated in cart.")
        else:
            messages.warning(r, "No more stock available to add.")
    else:
        messages.warning(r, "Item not found in cart.")
    return redirect(cart)

def cart_remove(r,id):
    print('Removing from cart for product id:', id)
    user=r.user
    product = get_object_or_404(addproduct, id=id)
    cart_item = cartpro.objects.filter(user=user, product=product).first()
    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity = cart_item.quantity - 1
            cart_item.save()
            product.qty = product.qty + 1
            product.save()
            messages.success(r, "Item quantity decreased in cart.")
        else:
            cart_item.delete()  # Remove item from cart if quantity is 1
            product.qty = product.qty + 1
            product.save()
            messages.success(r, "Item removed from cart.")
    return redirect("cart")

def remove_cart(r, id):
    user = r.user
    product = addproduct.objects.filter(id=id).first()
    if product:
        cart_item = cartpro.objects.filter(user=user, product=product).first()
        if cart_item:
            cart_item.delete()
    return redirect('cart')

def checkout(r, id):
    user = r.user
    add = customer.objects.filter(user=user)
    buy_now_id = r.GET.get('buy_now')

    cart = []
    amount = 0
    buy_now_product = None

    if buy_now_id:
        product = get_object_or_404(addproduct, id=buy_now_id)
        value = product.discounted_price()
        cart.append({
            'product': product,
            'quantity': 1,
            'value': value
        })
        amount = value
        buy_now_product = product.id  # Save the product ID
    else:
        cart_items = cartpro.objects.filter(user=user)
        for p in cart_items:
            value = p.quantity * p.product.discounted_price()
            cart.append({
                'product': p.product,
                'quantity': p.quantity,
                'value': value
            })
            amount += value

    shipping_cost = 0 if amount > 500 else 70
    totalamount = amount + shipping_cost
    razoramount = totalamount * 100  # Convert to paise

    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    data = {
        "amount": razoramount,
        "currency": "INR",
        "receipt": "order_rcptid_11",
        "payment_capture": "1"
    }

    try:
        payment_response = client.order.create(data=data)
        order_id = payment_response.get('id')
        order_status = payment_response.get('status')

        if order_status == 'created':
            Payment = payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status,
                buy_now_product_id=buy_now_product  # Save the buy now product ID here
            )
            Payment.save()
        else:
            raise Exception(f"Order creation failed with status: {order_status}")
    except Exception as e:
        return render(r, 'checkout.html', {
            'cart': cart,
            'amount': amount,
            'add': add,
            'user': user,
            'totalamount': totalamount,
            'razoramount': razoramount,
            'error_message': "Error creating payment order. Please try again."
        })

    return render(r, 'checkout.html', {
        'cart': cart,
        'amount': amount,
        'add': add,
        'user': user,
        'totalamount': totalamount,
        'razoramount': razoramount,
        'order_id': order_id 
    })

# def checkout(request, id):
#     user = request.user
#     add = customer.objects.filter(user=user)
#     cart_items = cartpro.objects.filter(user=user)
#     cart = []
#     amount = 0
#     for p in cart_items:
#         value = p.quantity * p.product.discounted_price()
#         cart.append({
#             'product': p.product,
#             'quantity': p.quantity,
#             'value': value
#         })
#         amount += value
#     totalamount = amount + 70
#     return render(request, 'checkout.html', {'cart': cart,'amount':amount, 'add': add, 'user': user, 'totalamount': totalamount})

# def checkout(r,id):
#     user = r.user
#     add = customer.objects.filter(user=user)
#     cart_items=cartpro.objects.filter(user=user)
#     cart = []
#     amount = 0
#     for p in cart_items:
#         value = p.quantity * p.product.discounted_price()  
#         cart.append({
#             'product': p.product,
#             'quantity': p.quantity,
#             'value': value
#         })
#         amount = amount + value
#     totalamount = round(amount + 70, 2)
#     print("Total Amount (in Rs):", totalamount)
#     razoramount = int(totalamount * 100)
#     print("Amount passed to Razorpay (in Paise):", razoramount)

#     if razoramount < 100:  # Razorpay requires a minimum of 100 paise (Rs. 1)
#         return HttpResponse("Invalid amount. Amount should be at least Rs. 1", status=400)

#     client = razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
#     data = { "amount": razoramount, "currency": "INR", "receipt": "order_rcptid_12" }
#     payment_response = client.order.create(data=data)
#     print(payment_response)
#     # {'amount': 76800, 'amount_due': 76800, 'amount_paid': 0, 'attempts': 0, 'created_at': 1723205986, 'currency': 'INR', 'entity': 'order', 'id': 'order_OinYwy2lkocYW0', 'notes': [], 'offer_id': None, 'receipt': 'order_rcptid_12', 'status': 'created'} 
#     order_id = payment_response['id']
#     order_status = payment_response['status']
#     if order_status == 'created':
#         Payment = payment(
#             user = user,
#             amount = totalamount,
#             razorpay_order_id = order_id,
#             razorpay_payment_status = order_status
#         )
#         Payment.save()
#     return render(r,'checkout.html',{'cart':cart,'amount':amount,'add': add, 'user': user,'totalamount': totalamount})


logger = logging.getLogger(__name__)
RAZORPAY_KEY = 'rzp_test_tYx4noCg3FqPbR'
RAZORPAY_SECRET = 'gVRoYReOx84vcs0Td5mfHeqz'
@csrf_exempt
def payment_callback(request):
    if request.method == 'POST':
        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')

        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        payment_data = client.payment.fetch(payment_id)
        amount = payment_data['amount'] / 100
        status = payment_data['status']

        try:
            payment_instance = payment.objects.get(razorpay_order_id=order_id)

            if status == 'captured':
                payment_instance.razorpay_payment_id = payment_id
                payment_instance.amount = amount
                payment_instance.razorpay_payment_status = status
                payment_instance.paid = True
                payment_instance.save()

                # Retrieve one or more customer instances
                customer_instances = customer.objects.filter(user=payment_instance.user)

                if payment_instance.buy_now_product_id:
                    # Handle "Buy Now" product for each customer instance
                    product = get_object_or_404(addproduct, id=payment_instance.buy_now_product_id)
                    for customer_instance in customer_instances:
                        orderplaced.objects.create(
                            user=payment_instance.user,
                            Customer=customer_instance,
                            product=product,
                            quantity=1,
                            Payment=payment_instance,
                            status='Pending'
                        )
                    product.qty -= 1
                    product.save()
                else:
                    # Handle cart items for each customer instance
                    cart_items = cartpro.objects.filter(user=payment_instance.user)
                    for customer_instance in customer_instances:
                        for item in cart_items:
                            orderplaced.objects.create(
                                user=payment_instance.user,
                                Customer=customer_instance,
                                product=item.product,
                                quantity=item.quantity,
                                Payment=payment_instance,
                                status='Pending'
                            )
                            item.product.qty -= item.quantity
                            item.product.save()
                            

                    cart_items.delete()

                return render(request, 'orderSuccess.html', {
                    'payment_id': payment_id,
                    'order_number': payment_instance.razorpay_order_id,
                    'cart_items': orderplaced.objects.filter(Payment=payment_instance),
                })
            else:
                messages.error(request, "Payment failed or was not captured. Please try again.")
                return redirect('index')

        except payment.DoesNotExist:
            messages.error(request, "Payment instance not found. Please try again.")
            return redirect('index')

    else:
        return HttpResponse(status=400)

# def payment_done(r):
#     order_id=r.GET.get('order_id')
#     payment_id=r.GET.get('payment_id')
#     cust_id=r.GET.get('cust_id')
#     user=r.user
#     Customer=customer.objects.get(id=cust_id)
#     Payment=payment.objects.get(razorpay_order_id=order_id)
#     Payment.paid=True
#     Payment.razorpay_payment_id=payment_id
#     Payment.save()
#     Cart=cartpro.objects.filter(user=user)
#     for c in cart:
#         orderplaced(user=user,customer=customer,product=c.product,quantity=c.quantity,payment=payment).save()
#         c.delete()

#     return redirect(order)


# @login_required
def order(r):
    print(r.user)
    user=r.user
    # order_placed = orderplaced.objects.all()
    order_placed=orderplaced.objects.filter(user=user)

    for order in order_placed:
        order.has_reviewed=Review.objects.filter(user=user,book=order.product).exists()
      
    return render(r,'order.html',{'order_placed':order_placed,'CATEGORY_CHOICES': addproduct.CATEGORY_CHOICES})

def add_review(r, book_id):
    totalitem = 0
    wishitem = 0
    if r.user.is_authenticated:
        totalitem = cartpro.objects.filter(user=r.user).count()
        wishitem = wishlist.objects.filter(user=r.user).count()
    book = addproduct.objects.get(id=book_id)
    if r.method == 'POST':
        form = ReviewForm(r.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = r.user
            review.book = book
            review.save()
            return redirect('book_detail', book_id=book.id)
    else:
        form = ReviewForm()
    return render(r, 'add_review.html', {'form': form, 'book': book,'CATEGORY_CHOICES': addproduct.CATEGORY_CHOICES,'totalitem': totalitem,'wishitem': wishitem})


@login_required
def view_wishlist(r):
    totalitem = 0
    wishitem = 0
    if r.user.is_authenticated:
        totalitem = cartpro.objects.filter(user=r.user).count()
        wishitem = wishlist.objects.filter(user=r.user).count()
    wishlist_items = wishlist.objects.filter(user=r.user)
    return render(r, 'wishlist.html', {'wishlist_items': wishlist_items,'CATEGORY_CHOICES': addproduct.CATEGORY_CHOICES,'totalitem':totalitem,'wishitem':wishitem})

@login_required
def add_to_wishlist(r, product_id):
    product = get_object_or_404(addproduct, id=product_id)
    wishlist.objects.get_or_create(user=r.user, product=product)
    return redirect('view_wishlist')

@login_required
def remove_from_wishlist(r, product_id):
    product = get_object_or_404(addproduct, id=product_id)
    wishlist.objects.filter(user=r.user, product=product).delete()
    return redirect( 'view_wishlist')


# @login_required
# def add_to_wishlist(request, product_id):
#     product = get_object_or_404(addproduct, id=product_id)
#     wishlist.objects.get_or_create(user=request.user, product=product)
#     return redirect('wishlist')

# @login_required
# def view_wishlist(request):
#     wishlist_items = wishlist.objects.filter(user=request.user)
#     return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

# @login_required
# def remove_from_wishlist(request, product_id):
#     product = get_object_or_404(addproduct, id=product_id)
#     wishlist.objects.filter(user=request.user, product=product).delete()
#     return redirect('wishlist')

def search(r):
    query = r.GET['search']
    product = addproduct.objects.filter(Q(title__contains=query))
    return render(r,'search.html')
    


def forgotpwd(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Generate and save a unique token
            token = get_random_string(length=32)  # Increase token length for security
            PasswordReset.objects.create(user=user, token=token)
            # Send email with reset link
            reset_link = f'http://127.0.0.1:8000/reset/{token}'
            send_mail(
                'Reset Your Password',
                f'Click the link to reset your password: {reset_link}',
                'settings.EMAIL_HOST_USER',
                [email],
                fail_silently=False
            )
            messages.success(request, 'A password reset link has been sent to your email address.')
        except User.DoesNotExist:
            messages.error(request, 'Email address is not registered.')
        except Exception as e:
            print(f'Error: {e}')
            messages.error(request, 'Network error. Please try again later.')
    
    return render(request, 'forgotpwd.html')


def pwdresetdone(r):
    return render(r,'pwdresetdone.html')
    
def reset_password(request, token):
    try:
        # Verify token and get associated user
        password_reset = PasswordReset.objects.get(token=token)
        user = User.objects.get(id=password_reset.user_id)
        
        if request.method == 'POST':
            new_password = request.POST.get('newpassword')
            repeat_password = request.POST.get('cpassword')
            
            if new_password != repeat_password:
                messages.error(request, 'Passwords do not match.')
            else:
                user.set_password(new_password)
                user.save()
                # Optionally, delete the password reset token
                # password_reset.delete()
                messages.success(request, 'Password has been reset successfully.')
                return redirect('login')
        
    except PasswordReset.DoesNotExist:
        messages.error(request, 'Invalid or expired token.')
        return redirect('forgot_password')  
    except User.DoesNotExist:
        messages.error(request, 'User associated with this token does not exist.')
        return redirect('forgot_password')  

    return render(request, 'reset_password.html', {'token': token})
    
def logout(r):
    usrlogout(r)
    return redirect(index)

def about_us(r):
    totalitem = 0
    wishitem = 0
    if r.user.is_authenticated:
        totalitem = cartpro.objects.filter(user=r.user).count()
        wishitem = wishlist.objects.filter(user=r.user).count()
    return render(r, 'about_us.html',{'CATEGORY_CHOICES': addproduct.CATEGORY_CHOICES,'totalitem':totalitem,'wishitem':wishitem})

def contact_us(r):
    totalitem = 0
    wishitem = 0
    if r.user.is_authenticated:
        totalitem = cartpro.objects.filter(user=r.user).count()
        wishitem = wishlist.objects.filter(user=r.user).count()

    if r.method == 'POST':
        form = ContactForm(r.POST)
        if form.is_valid():
            form.save()
            messages.success(r, 'Your message has been sent successfully!')
            return redirect('contact_us')
    else:
        form = ContactForm()

    return render(r, 'contact_us.html', {'form': form, 'CATEGORY_CHOICES': addproduct.CATEGORY_CHOICES,'totalitem':totalitem,
        'wishitem':wishitem})