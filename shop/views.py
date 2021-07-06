from django.shortcuts import render
from .models import Product, Contact, Orders, OrderUpdate
from math import ceil
import json

# Create your views here.
from django.http import HttpResponse

def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])


    params = {'allProds':allProds}
    return render(request, 'shop/index.html', params)

def about(request):

    return render(request, 'shop/about.html')

def contact(request):
    thank = False
    if request.method=='POST':
        print(request)
        name=request.POST.get('name', '')

        email=request.POST.get('email', '')
        phone=request.POST.get('phone', '')
        desc=request.POST.get('desc', '')
        contact=Contact(name=name, email=email, phone=phone, desc=desc)
        thank = True
        contact.save()
    return render(request,'shop/contact.html',{'thank':thank})

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')



def searchMatch(query, item):
    '''return true only if query matches the item '''
    if query in item.desc.lower() or query in  item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query =  request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item) ]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    parms = {'allProds':allProds, 'msg':""}
    if len(allProds)==0 or len(query):
        params = {'msg':"Search didn't found plese make sure to enter relevent search"}

    return render(request,'shop/search.html',parms)

def prodview(request,id):
    #fetch the product using id
    product = Product.objects.filter(id=id)
    return render(request,'shop/prodview.html',{'product':product[0]})

def checkout(request):
        if request.method=='POST':
            print(request)
            items_json=request.POST.get('itemsjson', '')
            name=request.POST.get('name', '')
            email=request.POST.get('email', '')
            address=request.POST.get('address', '')
            city=request.POST.get('city', '')
            state=request.POST.get('state', '')
            zip_code=request.POST.get('zip_code', '')
            phone=request.POST.get('phone', '')
            order=Orders(items_json=items_json, name=name, email=email, address=address, city=city, state=state, zip_code=zip_code, phone=phone)
            order.save()
            update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
            update.save()
            thank = True
            id = order.order_id
            return render(request,'shop/checkout.html',{'thank':thank, 'id':id})
        return render(request,'shop/checkout.html')
