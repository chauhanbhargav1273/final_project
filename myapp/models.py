from django.db import models

# Create your models here.
class user(models.Model):
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	email=models.EmailField()
	mobile=models.PositiveIntegerField()
	address=models.TextField()
	password=models.CharField(max_length=100)
	profile_pic=models.ImageField(upload_to= "profile_pic/",default="")
	usertype=models.CharField(max_length=100,default="buyer")
	admin_access=models.BooleanField(default=False)

	def __str__(self):
		return self.fname



class product(models.Model):
	seller=models.ForeignKey(user,on_delete=models.CASCADE)
	choice1=(
		("vagetables","vagetables"),
		("fruits","fruits"),
		("juice","juice"),
		("dried","dried"),

	)
	product_category=models.CharField(max_length=100,choices=choice1)
	product_name=models.CharField(max_length=100)
	product_price=models.PositiveIntegerField()
	product_desc=models.TextField()
	product_image=models.ImageField(upload_to="product_image/",default="")

	def __str__(self):
		return self.seller.fname+ "-"+self.product_name


class Wishlist(models.Model):
	users=models.ForeignKey(user,on_delete=models.CASCADE)
	products=models.ForeignKey(product,on_delete=models.CASCADE)


	def __str__(self):
		return self.users.fname+"-"+self.products.product_name



class Cart(models.Model):
	users=models.ForeignKey(user,on_delete=models.CASCADE)
	products=models.ForeignKey(product,on_delete=models.CASCADE)
	product_price=models.PositiveIntegerField()
	product_qty=models.PositiveIntegerField(default=1)
	total_price=models.PositiveIntegerField()
	payment_status=models.BooleanField(default=False)

	def __str__(self):
		return self.users.fname+"-"+self.products.product_name