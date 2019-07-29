from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import product

# Create your views here.
def home(request):
    projects = product.objects
    return render(request,'products/home.html',{'product':projects})


@login_required(login_url="/accounts/signup")
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['body'] and request.POST['url'] and request.FILES['image'] and request.FILES['icon']:
            products = product()
            products.title = request.POST['title']
            products.body = request.POST['body']
            if request.POST['url'].startswith("http://") or request.POST['url'].startswith("https://"):
                products.url = request.POST['url']
            else:
                products.url = "http://" + request.POST['url']
            products.image = request.FILES['image']
            products.icon = request.FILES['icon']
            products.pub_date = timezone.datetime.now()
            products.hunter = request.user
            products.save()
            return redirect('/products/' + str(products.id))
        else:
            return render(request,'products/create.html',{'error':'All fields are required!'})
    else:

        return render(request,'products/create.html')

def detail(request, products_id):
    products = get_object_or_404(product , pk=products_id)
    return render(request,'products/detail.html',{'product':products})

@login_required(login_url="/accounts/signup")
def upvote(request, products_id):
    if request.method == 'POST':
        products = get_object_or_404(product , pk=products_id)
        products.votes += 1
        products.save()
        return redirect('/products/' + str(products.id))
