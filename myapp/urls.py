from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('news/',views.news,name='news'),
    path('shop/',views.shop,name='shop'),
    path('about/',views.about,name='about'),
    path('single-news/',views.single_news,name='single-news'),
    path('seller-index',views.seller_index,name='seller-index'),
    path('single-product/<int:pk>/',views.single_product,name='single-product'),
    path('contact/',views.contact,name='contact'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('change-password/',views.change_password,name='change-password'),
    path('forgot-password/',views.forgot_password,name='forgot-password'),
    path('verify-otp/',views.verify_otp,name='verify-otp'),
    path('new-password/',views.new_password,name='new-password'),
    path('profile/',views.profile,name='profile'),
    path('view-vagetables',views.view_vagetables,name='view-vagetables'),
    path('view-fruits',views.view_fruits,name='view-fruits'),
    path('view-vagetables',views.view_vagetables,name='view-vagetables'),
    path('view-juice',views.view_juice,name='view-juice'),
    path('view-dried',views.view_dried,name='view-dried'),



    path('seller-add-product/',views.seller_add_product,name='seller-add-product'),
    path('seller-view-product/',views.seller_view_product,name='seller-view-product'),
    path('seller-product-detail/<int:pk>/',views.seller_product_detail,name='seller-product-detail'),
    path('seller-edit-product/<int:pk>/',views.seller_edit_product,name='seller-edit-product'),
    path('seller-delete-product/<int:pk>/',views.seller_delete_product,name='seller-delete-product'),
    path('seller-view-vagetables/',views.seller_view_vagetables,name='seller-view-vagetables'),
    path('seller-view-fruits/',views.seller_view_fruits,name='seller-view-fruits'),
    path('seller-view-juice/',views.seller_view_juice,name='seller-view-juice'),
    path('seller-view-dried/',views.seller_view_dried,name='seller-view-dried'),


    path('product-detail/<int:pk>/',views.product_detail,name='product-detail'),
    path('add-to-wishlist/<int:pk>/',views.add_to_wishlist,name='add-to-wishlist'),
    path('wishlist',views.wishlist,name='wishlist'),
    path('remove-from-wishlist/<int:pk>/',views.remove_from_wishlist,name='remove-from-wishlist'),
    path('add-to-cart/<int:pk>/',views.add_to_cart,name='add-to-cart'),
    path('cart',views.cart,name='cart'),
    path('remove-from-cart/<int:pk>/',views.remove_from_cart,name='remove-from-cart'),
    path('change-qty/',views.change_qty,name='change-qty'),
    path('success.html/', views.success,name='success'),
    path('cancel.html/', views.cancel,name='cancel'),
    path('myorder/',views.myorder,name='myorder'),
    path('create-checkout-session/', views.create_checkout_session, name='payment'),

    
    path('seller-view-order',views.seller_view_order,name='seller-view-order'),
    path('ajax/validate_email/',views.validate_signup,name='vlidate_email'),
    path('ajax/validate_login/',views.validate_login,name='validate_login'),
    path('ajax/oldpass/',views.oldpass,name='oldpass'),
    path('ajax/addpro/',views.addpro,name='addpro'),

]
