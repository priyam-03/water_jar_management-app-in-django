import razorpay
from .models import Order, ProductInOrder, Cart
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.shortcuts import HttpResponseRedirect
from .models import Water, Cost, CustomUser
from datetime import datetime
from .form import CustomUserCreationForm, CustomUserChangeForm


def signup(request):
    if request.CustomUser.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})


def home(request):
    return render(request, 'home.html')


def entry(request):
    current_time = datetime.today().strftime('%Y-%m-%d')
    data = {"current_time": current_time}
    return render(request, 'entry.html', data)


def log_in(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/dashboard')  # profile
        else:
            msg = 'Error Login'
            form = AuthenticationForm(request.POST)
            return render(request, 'login.html', {'form': form, 'msg': msg})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})


def signout(request):
    logout(request)
    return redirect('/')


def dashboard(req):
    current_user = req.user
    data = list(Water.objects.filter(User_id=current_user.id))
    return render(req, 'dashboard.html')


def savewater(req):
    # if req.method == "post":
    User_id = req.POST['userid']
    date = req.POST['date']
    quantity = req.POST['quantity']

    obj = Water.objects.create(
        User_id=User_id, date=date, quantity=quantity)
    message = ""

    if obj.id > 0:
        data = {"message": "Success"}
    else:
        data = {"message": "Failed"}
    current_time = datetime.today().strftime('%Y-%m-%d')

    data1 = {"data": data, "current_time": current_time}
    return render(req, 'entry.html', data1)
    # else:
    #     current_time = datetime.today().strftime('%Y-%m-%d')
    #     data = {"current_time": current_time}
    #     return render(req, 'entry.html', data)


def edit(req):
    id = req.POST['id1']
    User_id = req.POST['userid1']
    quantity = req.POST['quantity1']

    obj = Water.objects.get(id=id)

    obj.user = User_id
    obj.quantity = quantity
    obj.save()

    user = Water.objects.all()
    table = {"allusers": list(user)}
    data = {"table": table}
    return render(req, "jarhistory.html", data)


def jarhistory(req):
    user = Water.objects.all()
    table = {"allusers": list(user)}
    return render(req, "jarhistory.html", table)


def editcost(req):

    cost = req.POST['cost']

    obj = Cost.objects.get(id=2)
    obj.cost = cost

    obj.save()
    current_time = datetime.today().strftime('%Y-%m-%d')
    user = Water.objects.all()
    table = {"allusers": list(user)}
    cost = Cost.objects.get(id=2)
    data = {"current_time": current_time, "table": table, "cost2": cost}
    return render(req, "entry.html", data)


def admindashboard(req):
    user = Water.objects.all()
    table = {"allusers": list(user)}
    cost = Cost.objects.get(id=2)
    data1 = {
        "table": table, "cost2": cost}
    return render(req, 'admindashboard.html', data1)


razorpay_client = razorpay.Client(
    auth=(settings.razorpay_id, settings.razorpay_account_id))


@login_required
def payment(request):
    if request.method == "POST":
        try:
            cart = Cart.objects.get(user=request.user)
            products_in_cart = ProductInCart.objects.filter(cart=cart)
            final_price = 0
            if(len(products_in_cart) > 0):
                order = Order.objects.create(user=request.user, total_amount=0)
                # order.save()
                for product in products_in_cart:
                    product_in_order = ProductInOrder.objects.create(
                        order=order, product=product.product, quantity=product.quantity, price=product.product.price)
                    final_price = final_price + \
                        (product.product.price * product.quantity)
            else:
                return HttpResponse("No product in cart")
        except:
            return HttpResponse("No product in cart")

        order.total_amount = final_price
        order.save()

        order_currency = 'INR'

        callback_url = 'http://' + \
            str(get_current_site(request))+"/handlerequest/"
        print(callback_url)
        notes = {'order-type': "basic order from the website", 'key': 'value'}
        razorpay_order = razorpay_client.order.create(dict(
            amount=final_price*100, currency=order_currency, notes=notes, receipt=order.order_id, payment_capture='0'))
        print(razorpay_order['id'])
        order.razorpay_order_id = razorpay_order['id']
        order.save()

        return render(request, 'firstapp/payment/paymentsummaryrazorpay.html', {'order': order, 'order_id': razorpay_order['id'], 'orderId': order.order_id, 'final_price': final_price, 'razorpay_merchant_id': settings.razorpay_id, 'callback_url': callback_url})
    else:
        return HttpResponse("505 Not Found")
