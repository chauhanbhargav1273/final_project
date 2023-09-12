from django.contrib import admin
from .models import user,product,Wishlist,Cart,Contact
# Register your models here.
admin.site.register(user)
admin.site.register(product)
admin.site.register(Wishlist)
admin.site.register(Cart)
admin.site.register(Contact)


