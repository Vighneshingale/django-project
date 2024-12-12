from django.contrib import admin
from django.urls import path, include
from app1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Register',views.Register),
    path('login', views.user_login),
    path('logout', views.user_logout),
    path('About', views.about_us),
    path('Contact', views.Contact_us),
    path('feedback', views.feedback),
    path('Home', views.Home),
    path('product<pid>', views.products),
    path('cart<pid>', views.cart),
    path('Menu<cv>', views.Menu),
    path('viewcart',views.viewcart),
    path('updateqty/<x>/<cid>',views.updateqty),
    path('removecart<cid>',views.removecart),

   
]