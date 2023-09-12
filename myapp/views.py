from django.shortcuts import render,redirect
from .models import user,product,Wishlist,Cart,Contact
import requests
import random
import stripe
from django.conf import settings
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

stripe.api_key = settings.STRIPE_PRIVATE_KEY
YOUR_DOMAIN = 'http://localhost:8000'

def validate_signup(request):
	email=request.GET.get('email')
	data={
	'is_taken':user.objects.filter(email__iexact=email).exists()
	}
	return JsonResponse(data)

def validate_login(request):
	email=request.GET.get('email')
	data={
	'is_taken':user.objects.filter(email__iexact=email).exists()
	}
	return JsonResponse(data)

def oldpass(request):
	oldpass=request.GET.get('oldpass')
	users=user.objects.get(email=request.session['email'])
	flag=False
	if users.password==oldpass:
		flag=True
	data={
	'is_taken':flag
	}
	return JsonResponse(data)

def addpro(request):
	product_name=request.GET.get('addpro')
	seller=user.objects.get(email=request.session['email'])
	data={
	'is_taken':product.objects.filter(product_name__iexact=product_name,seller=seller).exists()
	}
	return JsonResponse(data)


@csrf_exempt
def create_checkout_session(request):
	amount = int(json.load(request)['post_data'])
	final_amount=amount*100
	
	session = stripe.checkout.Session.create(
		payment_method_types=['card'],
		line_items=[{
			'price_data': {
				'currency': 'inr',
				'product_data': {
					'name': 'Checkout Session Data',
					},
				'unit_amount': final_amount,
				},
			'quantity': 1,
			}],
		mode='payment',
		success_url=YOUR_DOMAIN + '/success.html',
		cancel_url=YOUR_DOMAIN + '/cancel.html',)
	return JsonResponse({'id': session.id})

def success(request):
	users=user.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(users=users,payment_status=False)
	for i in carts:
		i.payment_status=True
		i.save()
		
	carts=Cart.objects.filter(users=users,payment_status=False)
	request.session['cart_count']=len(carts)
	return render(request,'success.html')

def cancel(request):
	return render(request,'cancel.html')


# Create your views here.
def index(request):
	products=product.objects.all()
	try:
		users=user.objects.get(email=request.session['email'])
		if users.usertype=="buyer":
			return render(request,'index.html',{'products':products})
		else:
			return render(request,'seller-index.html',{'products':products})
	except:
		return render(request,'index.html',{'products':products})

def seller_index(request):
	seller=user.objects.get(email=request.session['email'])
	products=product.objects.filter(seller=seller)
	return render(request,'seller-index.html',{'products':products})

def news(request):
	return render(request,'news.html')

def about(request):
	return render(request,'about.html')

def single_news(request):
	return render(request,'single-news.html')

def single_product(request,pk):
	wishlist_flag=False
	cart_flag=False
	products=product.objects.get(pk=pk)
	try:
		users=user.objects.get(email=request.session['email'])
		try:
			Wishlist.objects.get(users=users,products=products)
			wishlist_flag=True
		except:
			pass
		try:
			Cart.objects.get(users=users,products=products)
			cart_flag=True
		except:
			pass
	except:
		pass
				

	return render(request,'single-product.html',{'products':products,'wishlist_flag':wishlist_flag,'cart_flag':cart_flag})


def shop(request):
	products=product.objects.all()
	return render(request,'shop.html',{'products':products})

def contact(request):
	if request.method=="POST":
		try:
			Contact.objects.get(email=request.POST['email'])
			msg="already exists"
			return render(request,'contact.html',{'msg':msg})
		except:
			Contact.objects.create(
				name=request.POST['name'],
				email=request.POST['email'],
				phone=request.POST['phone'],
				subject=request.POST['subject'],
				message=request.POST['message']
				)
			msg="contact saved sucessfully"
			return render(request,'contact.html',{'msg':msg})
	else:
		return render(request,'contact.html')

def signup(request):
	if request.method=="POST":
		try:
			print('hlo')
			print(request.POST['usertype'])
			user.objects.get(email=request.POST['email'])
			msg="email already registered"
			return render(request,'signup.html',{'msg':msg})
		except:
			if request.POST['password']==request.POST['cpassword']:
				if request.POST['usertype']=="buyer":
					admin_access=True
				else:
					admin_access=False
				user.objects.create(
					fname=request.POST['fname'],
					lname=request.POST['lname'],
					email=request.POST['email'],
					mobile=request.POST['mobile'],
					address=request.POST['address'],
					password=request.POST['password'],
					profile_pic=request.FILES['profile_pic'],
					usertype=request.POST['usertype'],
					admin_access=admin_access
					)
				msg="sign up sucessfully"
				return render(request,'signup.html',{'msg':msg})
			else:
				msg="password & confirm password does not match"
				return render(request,'signup.html',{'msg':msg})
	else:
		return render(request,'signup.html')


def login(request):
	if request.method=="POST":
		try:
			users=user.objects.get(email=request.POST['email'])
			if users.password==request.POST['password']:
				if users.usertype=="buyer":
					request.session['email']=users.email
					request.session['fname']=users.fname
					request.session['profile_pic']=users.profile_pic.url
					wishlists=Wishlist.objects.filter(users=users)
					request.session['wishlist_count']=len(wishlists)
					carts=Cart.objects.filter(users=users,payment_status=False)
					request.session['cart_count']=len(carts)
					return redirect('index')
				else:
					if users.admin_access==True:	
						request.session['email']=users.email
						request.session['fname']=users.fname
						request.session['profile_pic']=users.profile_pic.url
						return redirect('seller-index')
					else:
						msg="your admin access is still not approved. Please contact"
						return render(request,'login.html',{'msg':msg})
			else:
				msg="incorrect password"
				return render(request,'login.html',{'msg':msg})
		except:
			msg="email not registered"
			return render(request,'login.html',{'msg':msg})
	else:
		return render(request,'login.html')

def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		return redirect('index')
	except:
		return render(request,'login.html')


def change_password(request):
	users=user.objects.get(email=request.session['email'])
	if request.method=="POST":
		if users.password==request.POST['old-password']:
			if request.POST['new-password']==request.POST['cnew-password']:
				users.password=request.POST['new-password']
				users.save()
				return redirect('logout')
			else:
				msg="new password & confirm password does not match"
				if users.usertype=="buyer":
					return render(request,'change-password.html',{'msg':msg})
				else:
					return render(request,'seller-change-password.html',{'msg':msg})
		else:
			msg="old-password does not match"
			if users.usertype=="buyer":
				return render(request,'change-password.html',{'msg':msg})
			else:
				return render(request,'seller-change-password.html',{'msg':msg})
	else:
		if users.usertype=="buyer":
			return render(request,'change-password.html')
		else:
			return render(request,'seller-change-password.html')

def forgot_password(request):
	if request.method=="POST":
		mobile=request.POST['mobile']
		try:
			users=user.objects.get(mobile=mobile)
			otp=random.randint(1000,9999)
			url = "https://www.fast2sms.com/dev/bulkV2"
			querystring = {"authorization":"mIk9Ya7tBzZTeAU5C3VGyLwJuRH8ogc2xrqnsKMdPSib6W0jNlQCyZJVL4px2luo8hKgraUk9b3GWejM","variables_values":str(otp),"route":"otp","numbers":str(mobile)}	
			headers = {'cache-control': "no-cache"}
			response = requests.request("GET", url, headers=headers, params=querystring)
			print(response.text)
			return render(request,'otp.html',{'otp':otp,'mobile':mobile})
		except Exception as e:
			print(e)
			msg="mobile not registered"
			return render(request,'forgot-password.html',{'msg':msg})

	else:
		return render(request,'forgot-password.html')


def verify_otp(request):
	otp=request.POST['otp']
	uotp=request.POST['uotp']
	mobile=request.POST['mobile']
	if otp==uotp:
		return render(request,'new-password.html',{'mobile':mobile})
	else:
		msg="invalid OTP"
		return render(request,'otp.html',{'otp':otp,'mobile':mobile,'msg':msg})

def new_password(request):
	mobile=request.POST['mobile']
	np=request.POST['new-password']
	cnp=request.POST['cnew-password']

	if np==cnp:
		users=user.objects.get(mobile=mobile)
		users.password=np
		users.save()
		msg="update password sucessfully"
		return render(request,'login.html',{'msg':msg})
	else:
		msg="new password & confirm new-password does not match"
		return render(request,'new-password.html',{'mobile':mobile,'msg':msg})

def profile(request):
	users=user.objects.get(email=request.session['email'])
	if request.method=="POST":
		users.fname=request.POST['fname']
		users.lname=request.POST['lname']
		users.email=request.POST['email']
		users.mobile=request.POST['mobile']
		users.address=request.POST['address']
		try:
			users.profile_pic=request.FILES['profile_pic']
		except:
			pass
		users.save()
		request.session['profile_pic']=users.profile_pic.url
		msg="updated profile sucessfully"
		if users.usertype=="buyer":
			return render(request,'profile.html',{'users':users,'msg':msg})
		else:
			return render(request,'seller-profile.html',{'users':users,'msg':msg})
	else:
		if users.usertype=="buyer":
			return render(request,'profile.html',{'users':users})
		else:
			return render(request,'seller-profile.html',{'users':users})

def view_vagetables(request):
	users=user.objects.get(email=request.session['email'])
	products=product.objects.filter(product_category="vagetables")
	return render(request,'index.html',{'products':products})

def view_fruits(request):
	users=user.objects.get(email=request.session['email'])
	products=product.objects.filter(product_category="fruits")
	return render(request,'index.html',{'products':products})

def view_juice(request):
	users=user.objects.get(email=request.session['email'])
	products=product.objects.filter(product_category="juice")
	return render(request,'index.html',{'products':products})

def view_dried(request):
	users=user.objects.get(email=request.session['email'])
	products=product.objects.filter(product_category="dried")
	return render(request,'index.html',{'products':products})

def seller_add_product(request):
	seller=user.objects.get(email=request.session['email'])
	if request.method=="POST":
		product.objects.create(
				seller=seller,
				product_category=request.POST['product_category'],
				product_name=request.POST['product-name'],
				product_price=request.POST['product-price'],
				product_desc=request.POST['product-desc'],
				product_image=request.FILES['product-image'],
			)
		msg="add product sucessfully"
		return render(request,'seller-add-product.html',{'msg':msg})
	else:
		return render(request,'seller-add-product.html')


def seller_view_product(request):
	seller=user.objects.get(email=request.session['email'])
	products=product.objects.filter(seller=seller)
	return render(request,'seller_view_product.html',{'products':products})


def seller_product_detail(request,pk):
	products=product.objects.get(pk=pk)
	return render(request,'seller-product-detail.html',{'products':products})


def seller_edit_product(request,pk):
	products=product.objects.get(pk=pk)
	if request.method=="POST":
		products.product_category=request.POST['product_category']
		products.product_name=request.POST['product-name']
		products.product_price=request.POST['product-price']
		products.product_desc=request.POST['product-desc']
		try:
			products.product_image=request.FILES['product-image']
		except:
			pass
		products.save()
		msg="product update sucessfully"
		return render(request,'seller-edit-product.html',{'products':products,'msg':msg})
	else:
		return render(request,'seller-edit-product.html',{'products':products})


def seller_delete_product(request,pk):
	products=product.objects.get(pk=pk)
	products.delete()
	return redirect('seller-view-product')


def seller_view_vagetables(request):
	seller=user.objects.get(email=request.session['email'])
	products=product.objects.filter(seller=seller,product_category="vagetables")
	return render(request,'seller_view_product.html',{'products':products})

def seller_view_fruits(request):
	seller=user.objects.get(email=request.session['email'])
	products=product.objects.filter(seller=seller,product_category="fruits")
	return render(request,'seller_view_product.html',{'products':products})

def seller_view_juice(request):
	seller=user.objects.get(email=request.session['email'])
	products=product.objects.filter(seller=seller,product_category="juice")
	return render(request,'seller_view_product.html',{'products':products})

def seller_view_dried(request):
	seller=user.objects.get(email=request.session['email'])
	products=product.objects.filter(seller=seller,product_category="dried")
	return render(request,'seller_view_product.html',{'products':products})


def product_detail(request,pk):
	wishlist_flag=False
	cart_flag=False
	products=product.objects.get(pk=pk)
	try:
		users=user.objects.get(email=request.session['email'])
		try:
			Wishlist.objects.get(users=users,products=products)
			wishlist_flag=True
		except:
			pass
		try:
			Cart.objects.get(users=users,products=products)
			cart_flag=True
		except:
			pass
	except:
		pass
				

	return render(request,'product-detail.html',{'products':products,'wishlist_flag':wishlist_flag,'cart_flag':cart_flag})

def add_to_wishlist(request,pk):
	products=product.objects.get(pk=pk)
	users=user.objects.get(email=request.session['email'])
	Wishlist.objects.create(users=users,products=products)
	return redirect('wishlist')


def wishlist(request):
	users=user.objects.get(email=request.session['email'])
	wishlists=Wishlist.objects.filter(users=users)
	request.session['wishlist_count']=len(wishlists)
	return render(request,'wishlist.html',{'wishlists':wishlists})


def remove_from_wishlist(request,pk):
	products=product.objects.get(pk=pk)
	users=user.objects.get(email=request.session['email'])
	wishlists=Wishlist.objects.get(users=users,products=products)
	wishlists.delete()
	return redirect('wishlist')


def add_to_cart(request,pk):
	products=product.objects.get(pk=pk)
	users=user.objects.get(email=request.session['email'])
	Cart.objects.create(
		users=users,
		products=products,
		product_price=products.product_price,
		product_qty=1,
		total_price=products.product_price,
	)
	return redirect('cart')


def cart(request):
	net_price=0
	users=user.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(users=users,payment_status=False)
	request.session['cart_count']=len(carts)
	for i in carts:
		net_price=net_price+i.total_price
	return render(request,'cart.html',{'carts':carts,'net_price':net_price})


def remove_from_cart(request,pk):
	products=product.objects.get(pk=pk)
	users=user.objects.get(email=request.session['email'])
	carts=Cart.objects.get(users=users,products=products,payment_status=False)
	carts.delete()
	return redirect('cart')

def change_qty(request):
	pk=int(request.POST['pk'])
	carts=Cart.objects.get(pk=pk,payment_status=False)
	product_qty=int(request.POST['product_qty'])
	carts.product_qty=product_qty
	carts.total_price=carts.product_price*product_qty
	carts.save()
	return redirect('cart')

def myorder(request):
	users=user.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(users=users,payment_status=True)
	return render(request,'myorder.html',{'carts':carts})


def seller_view_order(request):
	myorder = []
	seller=user.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(payment_status=True)
	for i in carts:
		myorder.append(i)	
	return render(request,'seller-view-order.html',{'carts':carts})


