
from django.shortcuts import render
from django.http import HttpResponse
from .models import product, Contact
from  math import ceil

# Create your views here.
def index (request):
    allprods = []
    catprods = product.objects.values('category' , 'id')
    cats = {item ['category'] for item in catprods}
    for cat in cats:
        prod = product.objects.filter(category = cat)
        n = len(prod)
        nslides = n // 4 + ceil((n / 4) - (n // 4))
        allprods.append([prod, range(1,nslides),nslides])

    #params = {'no_of_slides': nslides , 'range' : range(1,nslides) , 'product':products  }
    # allprods = [[products, range(1,len(products)),nslides],[products, range(1,len(products)),nslides] ]
    params = {'allprods': allprods}
    return render(request,'shop/index1.html' ,params)

def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query)<4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)




def about (request):
    return render(request,'shop/about.html')
# def about (request):
#     return HttpResponse("We are at here about")


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        desc = request.POST.get('desc', '')
        print(name,email,phone,desc)
        contact = Contact(name=name , phone=phone, email=email, desc=desc)
        contact.save()

    return render(request, 'shop/contact.html')


def tracker  (request):
    return render(request, 'shop/tracker.html')




def  proview (request ,myid):
    products = product.objects.filter(id=myid)
    return render(request,'shop/proview.html', {'product':products[0]})


def check (request):
     return render(request,'shop/check.html')

