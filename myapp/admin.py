from django.contrib import admin
from .models import user,product,Wishlist,Cart
# Register your models here.
admin.site.register(user)
admin.site.register(product)
admin.site.register(Wishlist)
admin.site.register(Cart)

