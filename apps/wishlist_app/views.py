from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.contrib import messages

def index(request):
    return render(request,'wishlist_app/index.html')
    

def register(request):
    result = User.objects.validate_registration(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request,err)
        return redirect('/')
    request.session['user_id'] = result.id
    #print result.id
    # messages.success(request, "Successfully registered!")
    return render(request,'wishlist_app/dashboard.html')


def login(request):
    result = User.objects.validate_login(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    # messages.success(request, "Successfully logged in!")
    return redirect('/show_dashboard')

def add_show(request,id):
    
    content = {
        'user' : User.objects.get(id = id)
    }
    return render(request,'wishlist_app/create_list.html',content)

def show_dashboard(request):
    content = {
        'user' : User.objects.get(id = request.session['user_id']),
        'products':User.objects.get(id = request.session['user_id']).wish.all(),
        'alls': List.objects.exclude(added_by_id =request.session['user_id']) 
        
    }
    
    return render(request,'wishlist_app/dashboard.html',content)
    
def create_list(request):
    user_id= request.session['user_id']
    print user_id
    # content = {
    #     'user' : User.objects.get(id = request.session['user_id'])
    # }
    if len(request.POST['product']) < 1:
        messages.error(request,'EMPTY FIELD')
    if len(request.POST['product']) < 3:
        messages.error(request,'Should be more then 3 character')
        return redirect('/wish_items/create/'+ str(user_id)  )
    user = User.objects.get(id = request.session['user_id'])
    l = List.objects.create(product_name = request.POST['product'],added_by = user)
    l.wished_by.add(user)


    return redirect('/show_dashboard')

def show_product(request,id):
    content = {
        'products' : List.objects.get(id = id),
        'users' : List.objects.get(id = id).wished_by.all()
    }
    return render(request,'wishlist_app/show_list.html',content)

def add_list(request ,id):
    list = List.objects.get(id= id)
    user = User.objects.get(id = request.session['user_id'])
    list.wished_by.add(user)
    return redirect('/show_dashboard')


def remove(request,id,product_id):
    
    if int(id) == request.session['user_id']:
        
        List.objects.get(id=product_id).delete()
    else:
        user = User.objects.get(id=request.session['user_id'])
        list = List.objects.get(id =product_id)
        list.wished_by.remove(user)

    return redirect('/show_dashboard')
      
