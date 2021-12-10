from django.shortcuts import render,redirect
from django.conf import settings
import datetime
from django.views.decorators.csrf import csrf_exempt
import razorpay
import stripe
from payments.models import Order
import socket

stripe.api_key =settings.STRIPE_SKEY
# Create your views here.
def interface(request):
    return render(request,"interface.html")

def load_raz(request):
    if(request.method=='POST'):
        return render(request,"raz_con.html",{'amountp':str(int(request.POST['amount'])*100),'amountr':request.POST['amount'],'name':request.POST['name'],'email':request.POST['email']})
    else:
        return render(request,"razorpay.html")

@csrf_exempt
def razcon(request):
    if(request.method=='POST'):
        DATA = {
        "amount": int(request.POST['amount'])*100,
        "currency": "INR",
        "payment_capture": "1",
        }
        client = razorpay.Client(auth=(settings.RAZORPAY_ID, settings.RAZORPAY_KEY))
        payment=client.order.create(data=DATA)
        order=Order()
        order.payment_id=payment['id']
        order.name=request.POST['name']
        order.email=request.POST['email']
        order.amount=request.POST['amount']
        order.method='Razorpay'
        order.save()
        return redirect('success')
    else:
        return render(request,"raz_con.html")

DOMAIN=socket.gethostname()
def load_stri(request):
    if(request.method=='POST'):
        price=int(request.POST['amount'])*100
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency':'inr',
                        'unit_amount':price,
                        'product_data':{
                            'name':request.POST['name']
                        }
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=DOMAIN + '/success',
            cancel_url=DOMAIN + '/cancel',
        )
        order=Order()
        order.payment_id=checkout_session['payment_intent']
        order.name=request.POST['name']
        order.email=request.POST['email']
        order.amount=request.POST['amount']
        order.method='Stripe'
        order.save()
        print(checkout_session)
        return redirect(checkout_session.url)
    return render(request,"stripe.html")

def success(request):
    return render(request,"success.html")

def cancel(request):
    return render(request,"cancel.html")