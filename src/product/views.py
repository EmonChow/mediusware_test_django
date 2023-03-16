from django.shortcuts import render,redirect
from product import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import inlineformset_factory
from product import forms
from django.contrib import messages


# Create your views here.
def home_view(request):
   
    products=models.Product.objects.all()
    product_num = products.count()
   
    variant = models.Variant.objects.all()
    
  
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 2)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context={
        'products':products,
        'product_num':product_num,
        'variant':variant
    }
    return render(request, 'home.html',context)

# search bar 
def search_view(request):
    if request.method == 'GET':
        search = request.GET.get('inputTitle') 
        dropdown = request.GET.get('dropdown')
        priceFrom = request.GET.get('from') 
        priceTo = request.GET.get('to')
      
        if (priceFrom !=''):
            priceFrom = int(priceFrom)
        else:
            priceFrom = 0
        if (priceTo !=''):
            priceTo = int(priceTo)
        else:
            priceTo = 9999999
       
        searchItem = models.Product.objects.filter(productvariantprice__price__gte = priceFrom, productvariantprice__price__lte = priceTo).filter(title__contains = search).filter(productvariant__variant__title = dropdown)
        context = {
            'products':searchItem,
        }
    return render(request, 'search.html', context)

# add product page 
def add_product_view(request):
    productForm = forms.productForm
    ProductImageForm = forms.ProductImageForm
  
    ProductFormSet = inlineformset_factory(models.Product, models.ProductVariantPrice,
                                        fk_name='product',
                                        fields=('product_variant_one','product_variant_two','product_variant_three','price','stock'),
                                        extra=2)
    formset = ProductFormSet()
    if request.method=='POST':
        productForm = forms.productForm(request.POST, request.FILES)
       
        formset = ProductFormSet(request.POST, request.FILES)
      
        if productForm.is_valid() and formset.is_valid():
            product=productForm.save()
            pd=formset.save(commit=False)
            for p in pd:
                p.product=product
                p.save()
       
            messages.success(request, f"Product has been added")
            return redirect('home')
    context={
        'productForm':productForm,
        'ProductImageForm' : ProductImageForm,
        'formset':formset,
    }
    return render(request, 'product_add.html', context)


def edit_product(request, pk):
   
    product = models.Product.objects.get(id=pk)
    productForm = forms.productForm(instance=product)
    
  
    BookFormSet = inlineformset_factory(models.Product, models.ProductVariantPrice,
                                        fk_name='product',
                                        fields=('product_variant_one','product_variant_two','product_variant_three','price','stock'),
                                        extra=2)
    formset = BookFormSet(instance=product)
    
    if request.method=='POST':
        productForm = forms.productForm( request.POST, request.FILES, instance=product)
        formset = BookFormSet(request.POST, request.FILES, instance=product)
        if productForm.is_valid() and formset.is_valid():
            productForm.save()
            formset.save(commit=False)
            formset.instance=product
            formset.save()
         
            messages.success(request, f"Product has been updated")
            return redirect('home')
    context={
        'productForm':productForm,
        'formset':formset,
        
    }
    return render(request, 'edit_product.html',context)