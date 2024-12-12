import random
from urllib import request
from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

from app1.models import Product, Order, Cart
from django.db.models import Q


# Create your views here.

def Register(request):
    context = {}
    
    if request.method == "GET":
        return render(request, 'Register.html')
    else:
        n = request.POST['name']
        p = request.POST['password']
        cp = request.POST['cp']
       # print(n)
        #print(p)
        #print(cp)
        #return HttpResponse("Data Fetched !!!")
        if n == '' or p == '' or cp=='' :
            context['errmsg'] = "Fields cannot be empty"
            return render(request, 'Register.html', context)
        elif p!=cp:
            context['errmsg'] = "Password do not matched confirm password"
            return render(request, 'Register.html', context)
        elif len(p)<8 or len(p)>15:
            context['errmsg'] = "lenth of password gretter than 8 and less than 15"
            return render(request, 'Register.html', context)
        else:
            try:
                u= User.objects.create(username = n)
                u.set_password(p)
                u.save()
                context['success'] = "User registered sucessfully!!"
                return render(request, 'Register.html', context)
            
            except Exception as e:
                context['errmsg'] = "Already Registered, Please Login!!"
                return render(request, 'Register.html', context)

def user_login(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        n = request.POST['name']
        p = request.POST['password']
        u = authenticate(username = n , password = p)

        if u is not None:
            login(request, u)
            return redirect('/Home')
        else:
            context = {}
            context['errmsg'] = "Invalid user and password"
            return render(request, "login.html", context)
        
def user_logout(request):
    logout(request)
    return render("index.html")
        
def about_us(request):
    return render(request,"About.html")
def Contact_us(request):
    return render(request,"Contact us.html")
def feedback(request):
    return render(request,"feedback.html")
def Home(request):
    p = Product.objects.all()
    context = {}
    context["Product"] = p
    return render(request,"index.html",context)

def products(request,pid):
    p = Product.objects.filter(id=pid)
    context = {}
    context["Product"] = p
    return render(request,"product details.html",context)

# def sort(request, sv):
#     if sv == '1':
#         p = Product.objects.order_by('price').filter(is_active = True)
#     else:
#         p = Product.objects.order_by('price').filter(is_active = True)
#         context = {}
#         context[ 'data' ] = p
#         return render(request, "index.html", context)

def cart(request, pid):
    if request.user.is_authenticated:

        u = User.objects.filter(id = request.user.id)
        p = Product.objects.filter(id = pid )
        # print(u)
        # print(p)

        q1 = Q(user_id = u[0])
        q2 = Q(pid = p[0])
        c = Cart.objects.filter(q1 & q2)
        n = len(c)
        print(n)
        context= {}
        context[ 'Product' ] = p
        if n== 1:
            context['msg'] = n
        else:
            c= Cart.objects.create(user_id = u[0], pid = p[0])
            c.save()
            context['msg'] = n
           # return HttpResponse("product added to the cart!!")
        return render(request,"product details.html",context)
def Menu(request,cv):
    if cv == '1':
        obj=Product.objects.filter(cat='VEG DISHES')
        print(obj)
        context={'Product':obj}
        return render(request,'index.html',context)
    elif cv == '2':
        obj=Product.objects.filter(cat='NON-VEG DISHES')
        context={'Product':obj}
        return render(request,'index.html',context)
    elif cv == '3':
        obj=Product.objects.filter(cat='VEG STARTUP')
        context={'Product':obj}
        return render(request,'index.html',context)
    elif cv == '4':
        obj=Product.objects.filter(cat='NON_VEJ STARTUP')
        context={'Product':obj}
        return render(request,'index.html',context)
    elif cv == '5':
        obj=Product.objects.filter(cat='DESSERT')
        context={'Product':obj}
        return render(request,'index.html',context)
    elif cv == '6':
        obj=Product.objects.filter(cat='COLD-DRINKS')
        context={'Product':obj}
        return render(request,'index.html',context)
    else:
        obj=Product.objects.filter(cat='CHINESE')
        context={'Product':obj}
        return render(request,'index.html',context)
def viewcart(request):
    c=Cart.objects.filter(user_id = request.user.id)
    n = len(c)
    # q=c[0].qty
    # print(q)
    # print(c[0].qty)
    # print(c[0].user_id)
    # print(c[0].user_id.is_staff)
    # print(c[0].pid.name)
    total = 0
    n_p=0
    for x in c :
        total = total + x.pid.price * x.qty
        n_p = n_p + x.qty

    context={}
    context['cart']=c
   
    context["total"]=total
    # context['n']= n
    context['n']= n_p
    return render(request,"cart.html",context)

def updateqty(request, x, cid):
    print(x)
    print(cid)
    c = Cart.objects.filter(id=cid)
    q = c[0].qty
    print(q)
    if x == '1':
        q = q + 1
    elif q > 1 and x == "0":
        q = q - 1
    c.update(qty=q)
    return redirect("/viewcart")
def removecart(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect("/viewcart")
def placeorder(request):
    c=Cart.objects.Fields(id=request.user.id)
    oid=random.randrange(1000,9999)
    for x in c :
        ord=Order.objects.create(order_id=oid,qty=x.qty,user_id=x.user_id,amt=x.qty*x.pid)
        ord.save()
        x.delete()
    return redirect("/fetchedorderddetails")