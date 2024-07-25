# Import necessary modules
from django.shortcuts import render, redirect
from .forms import CommentForm
from django.db.models import F, Case, When, Value, IntegerField
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .models import Product, Cart,Review
from django.contrib.auth.decorators import login_required
from All_users.models import User
from django.core.paginator import Paginator




def home_page(request):
    books = Product.objects.all().order_by('-id')[:25]
    new_products = Product.objects.all().order_by('-id')[:8]
    last_Arrivals  = Product.objects.all().order_by('-id')[8:18]
    better_product  = Product.objects.annotate(
    has_discount=Case(
        When(discount_percentage__gt=0, then=Value(1)),
        default=Value(0),
        output_field=IntegerField(),
    )).order_by(
    '-has_discount',  # Products with discount come first
    '-discount_percentage'  # Within discounted products, higher discount comes first
    )[0:10]

    context = {
        'books': books,
        'new_products': new_products,
        'last_arrivals': last_Arrivals,
        'better_products': better_product,
    }

    return render(request, 'pages/index.html', context)


def shop_page(request,url):
    if request.method:
        sort_option = request.POST.get('sort_option')
    
        if sort_option == '1':
            all_products = Product.objects.order_by('name')
            sort = 1
        elif sort_option == '2':
            all_products = Product.objects.order_by('-name')
            sort = 2
        elif sort_option == '3':
            all_products = Product.objects.order_by('price_new')
            sort = 3
        elif sort_option == '4':
            all_products = Product.objects.order_by('-price_new')
            sort = 4
        elif sort_option == '5':
            all_products = Product.objects.order_by('reviews')
            sort = 5
        elif sort_option == '6':
            all_products = Product.objects.order_by('-reviews')
            sort = 6
        else:
            all_products = Product.objects.all().order_by('-id')
            sort = 0
    else:

        all_products = Product.objects.all().order_by('-id')

         
    all_products_count = Product.objects.all().order_by('-id').count()
    paginator = Paginator(all_products, 20)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)



    if url == "grid":
        return render(request, 'pages/shop-grid.html', {'all_products': page_obj,'this':'grid','count':all_products_count,"page_obj": page_obj,"sort_option":sort})
    elif url == "grand":
        return render(request, 'pages/shop-grid.html', {'all_products': page_obj,'this':'grand','count':all_products_count,"page_obj": page_obj,"sort_option":sort})
    elif url == "shop" :
        return render(request, 'pages/shop-list.html', {'all_products': page_obj,'this':'shop','count':all_products_count,"page_obj": page_obj,"sort_option":sort})

def detail_product(request, pid, id):
    product_off = list(Product.objects.annotate(
    has_discount=Case(
        When(discount_percentage__gt=0, then=Value(1)),
        default=Value(0),
        output_field=IntegerField(),
    )
).exclude(id=id).order_by(
    '-has_discount',  # Products with discount come first
    '-discount_percentage'  # Within discounted products, higher discount comes first
)[:8])

    product_name = list(Product.objects.filter(name__icontains=Product.objects.get(id=id).name).exclude(id=id).order_by('-id')[:8])
    product_name_set = set(product_name)
    product_off_set = set(product_off)

# Combine the two sets
    products = list(product_name_set.union(product_off_set))
    review = Review.objects.filter(product=id).exclude(userid=request.user.id).order_by('-id')
    product = Product.objects.get(pid=pid)
    review_count = Review.objects.filter(product=product).count()

    if Review.objects.filter(product=id, userid=request.user.id).exists():
        my_review = Review.objects.get(product=id, userid=request.user.id)
    else:
        my_review = None


    if request.method == 'POST':
        if request.user.is_authenticated:
            if 'btnform1' in request.POST:
                form = CommentForm(request.POST)
                selected_star = None
                for i in range(1, 7):
                    star_name = f'star{i}'
                    if request.POST.get(star_name) == 'on':
                        selected_star = i
                if selected_star != 6:       
                    if form.is_valid():
                        message = form.cleaned_data['message']
                        name = form.cleaned_data['name']
                        user = request.user.id
                        email = User.objects.get(id=user).email
                        if Review.objects.filter(product=product, userid=user).exists() :
                        # Create a review with the selected star rating
                            rev = Review.objects.get(product=product, userid=user)
                            rev.comment = message
                            rev.name = name
                            rev.email = email
                            rev.rate = selected_star
                            rev.save()
                            review = Review.objects.filter(product=id).order_by('-id')
                            product = Product.objects.get(pid=pid)
                            review_count = Review.objects.filter(product=product).count()
                            # Calculate average rating

                            total_ratings = sum([review.rate for review in review])
                            average_rating = round(total_ratings / review_count, 2)
                            Product.objects.filter(id=product.id).update(reviews=average_rating)
                            msg1 = "Your review has been successfully updated."
                            messages.success(request, msg1)
                            return redirect('base:product',id=id,pid=pid)

                        else:

                            review0 = Review(product=product,userid=user,comment=message,name=name,email=email,rate=selected_star)
                            review0.save()
                            review = Review.objects.filter(product=id).order_by('-id')
                            product = Product.objects.get(pid=pid)
                            review_count = Review.objects.filter(product=product).count()
                            # Calculate average rating

                            total_ratings = sum([review.rate for review in review])
                            average_rating = round(total_ratings / review_count, 2)
                            Product.objects.filter(id=product.id).update(reviews=average_rating)
                            msg = "Thanks for your review!"
                            messages.success(request, msg)
                            return redirect('base:product',id=id,pid=pid)
                            
                    else:
                        msg = "check your data"
                        messages.success(request, msg) 
                        return redirect('base:product',id=id,pid=pid)
                else:
                    pass  
            else:
                product_check = Product.objects.get(id=id)
                if product_check:
                    if Cart.objects.filter(user=request.user.id , product_id=id):
                        msg = "Product Already in Cart"
                        messages.success(request, msg)
                        return redirect("base:product",id=id,pid=pid)

                    else:
                        Cart.objects.create(user=request.user, product_id=id)
                        msg = "Product added successfully"
                        messages.success(request, msg)
                        return redirect("base:product",id=id,pid=pid)
                else:
                    msg = "No such product found"
                    messages.success(request, msg)
                    return redirect("base:product",id=id,pid=pid)
        else:
            
            return redirect('account:signup')
    else:
        
        form = CommentForm()


    return render(request, 'pages/product-details.html',{'prd':product,'form':form,'count':review_count,'review':review,'my_review':my_review,'product_off':products})


@login_required
def product_list(request):
    cart_items = Cart.objects.filter(user=request.user)  # Get all cart items for the current user
    products = []  # Initialize an empty list for products
    price = []
    for item in cart_items:
        products.append(item.product)
        price.append(item.product.price_new)
    product_off = Product.objects.annotate(
    has_discount=Case(
        When(discount_percentage__gt=0, then=Value(1)),
        default=Value(0),
        output_field=IntegerField(),
    )
).order_by(
    '-has_discount',  # Products with discount come first
    '-discount_percentage'  # Within discounted products, higher discount comes first
)[:8]
    somme = sum(price)
    return render(request, 'pages/product_list.html',{"products":products, 'product_off':product_off, 'sum':somme})

@login_required
def delete_item(request, pk):
        item = get_object_or_404(Cart, product_id=pk)
        if item.user == request.user:
            item.delete()            
            return redirect("base:cart")


@login_required
def add_to_cart(request,pk,url):
    product_check = Product.objects.get(id=pk)
    if product_check:
        if Cart.objects.filter(user=request.user.id , product_id=pk):
            pass
        else:
            Cart.objects.create(user=request.user, product_id=pk)
            
    return redirect("base:cart")

@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    price = []
    for item in cart_items:
        price.append(item.product.price_new)
    somme = sum(price)


    context= {
    'products':cart_items,
    'somme':somme
    }
    return render(request, 'pages/checkout.html', context)

