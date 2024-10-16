"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('adminindex/',views.admin_index, name='admin_index'),
    path('registerr/',views.register,name='register'),
    path('login/', views.login, name='login'),
    path('profile/',views.profile, name='profile'),
    path('address/',views.address, name='address'),
    path('updateAddress/<int:id>/',views.updateAddress, name='updateAddress'),
    path('delete/<int:id>/',views.delete, name='delete'),
    path('changepwd/', views.changepwd, name='changepwd'),
    path('pwdchangedone/',views.pwdchangedone, name='pwdchangedone'),
    path('addproduct/',views.addprod, name='addprod'),
    path('display/',views.prodisplay, name='prodisplay'),
    path('editpro/<int:id>/',views.editpro,name='editpro'),
    path('remove/<int:id>/',views.remove,name='remove'),
    path('adminstock/',views.admin_stock,name='adminstock'),
    path('update_stock/<int:product_id>/', views.update_stock, name='update_stock'),
    path('adminorders/',views.admin_orders,name='adminorders'),
    path('deleteorders/<int:order_id>',views.delete_order,name='deleteorders'),
    path('adminusers/', views.admin_users, name='adminusers'),
    path('deleteuser/<int:user_id>/', views.delete_user, name='deleteuser'),
    path('adminmessages/', views.admin_contact, name='adminmessages'),
    path('deletemessages/<int:id>/', views.delete_message, name='deletemessages'),
    path('forgotpwd/',views.forgotpwd,name='forgotpwd'),
    path('logout/',views.logout,name='logout'),
    path('reset/<token>',views.reset_password,name='reset_password'),
    path('pwdresetdone',views.pwdresetdone,name='pwdresetdone'),
    path('category/<str:category>',views.category_books, name='category_books'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('category/all/', views.all_books, name='all_books'),
    path('addtocart/',views.addtocart, name='addtocart'),
    path('cart/',views.cart,name='cart'),
    path('cart_update/<int:id>',views.cart_update,name='cart_update'),
    path('cart_remove/<int:id>',views.cart_remove,name='cart_remove'),
    path('remove_cart/<int:id>',views.remove_cart,name='remove_cart'),
    path('checkout/<int:id>',views.checkout,name='checkout'),
    path('payment_callback/', views.payment_callback, name='payment_callback'),
    path('order/',views.order,name='order'),
    path('book/<int:book_id>/add_review/', views.add_review, name='add_review'),
    path('wishlist/', views.view_wishlist, name='view_wishlist'),  
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('about-us/', views.about_us, name='about_us'),
    path('contact/', views.contact_us, name='contact_us'),
    # path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    # path('admin/add_book/', views.add_book, name='add_book'),
    # path('admin/update_stock/<int:book_id>/', views.update_stock, name='update_stock'),
    # path('', views.book_list, name='book_list'),
    # path('add_to_cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    # path('cart/', views.cart, name='cart'),
    # path('checkout/', views.checkout, name='checkout'),
    # path('order_history/', views.order_history, name='order_history'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
