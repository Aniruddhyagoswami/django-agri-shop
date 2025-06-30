from email import message
from itertools import product
import logging
from re import S
from django.db.models import Min
from django.contrib.sites.shortcuts import get_current_site
from datetime import timedelta
from django.contrib.auth.views import PasswordResetView
from django.core.mail import EmailMultiAlternatives
from urllib import response
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO
from portal.form import ProductForm
from .models import *
from decimal import Decimal
from collections import defaultdict
from django.views.decorators.http import require_POST
from django.db import transaction
from collections import defaultdict
from decimal import Decimal
from django.http import JsonResponse
from django.db.models import Q
from django.core import serializers
# Home Page
def get_filtered_cards(section_queryset, cards_queryset=None):
    """
    Returns unique CardDetails for a given section queryset.
    Optional: reuse a cards_queryset to avoid multiple DB hits.
    """
    product_names = list(dict.fromkeys(item.productname for item in section_queryset))

    card_ids = (CardDetails.objects
                .filter(cardtitle__in=product_names)
                .values('cardtitle')
                .annotate(min_id=Min('id'))
                .values_list('min_id', flat=True))

    return CardDetails.objects.filter(id__in=card_ids)


def get_subcatagory_filter(name):
    catagories=Catagoriesofitems.objects.get(Catagory_name=name)
    subcata=catagories.SubCatagoriesofitems.all()
    return subcata
        

def home(request):
    # Fetch categories, sliders
    catagories = Catagoriesofitems.objects.all()
    slider = Slidermaintain.objects.all()

    # Section models
    recommendations = Recomendations.objects.all()
    offersSection = OffersSection.objects.all()
    growthSection = GrowthSection.objects.all()
    smartfarmingSection = SmartfarmingSection.objects.all()
    spraySection = SpraySection.objects.all()
    seedsSection = SeedsSection.objects.all()
    seasonalSection = SeasonalSection.objects.all()

    # Filtered cards per section
    recomcard = get_filtered_cards(recommendations)
    offercard = get_filtered_cards(offersSection)
    growthcard = get_filtered_cards(growthSection)
    Smartfarmingcard = get_filtered_cards(smartfarmingSection)
    Spraycard = get_filtered_cards(spraySection)
    Seedscard = get_filtered_cards(seedsSection)
    seasonalcard = get_filtered_cards(seasonalSection)

    return render(request, "index.html", {
        'catagories': catagories,
        'slider': slider,
        'recomcard': recomcard,
        'offercard': offercard,
        'growthcard': growthcard,
        'Smartfarmingcard': Smartfarmingcard,
        'Spraycard': Spraycard,
        'Seedscard': Seedscard,
        'seasonalcard': seasonalcard,
    })



# About Us Page
def aboutus(request):
    catagories = Catagoriesofitems.objects.all()
    return render(request, "aboutus.html", {'catagories': catagories})

# Contact Page
def Contact(request):
    catagories = Catagoriesofitems.objects.all()
    return render(request, "contact.html", {'catagories': catagories})

# def Dynamic(request, name):
#     # 1. Always fetch all top‑level categories for your sidebar/nav
#     catagories = Catagoriesofitems.objects.all()

#     # 2. Prepare defaults
#     pagename    = name
    
#     card_qs     = CardDetails.objects.none()        # empty QuerySet
#     subcata_qs  = SubCatagoriesofitems.objects.none()
#     sort_option = request.GET.get('sort')

#     # 3. Is it a category page?
#     try:
#         cata = Catagoriesofitems.objects.get(Catagory_name=name)
#         # cards under this category
#         card_qs = CardDetails.objects.filter(category=cata)
#         # list all subcategories of this category
#         subcata_qs = SubCatagoriesofitems.objects.filter(category=cata)

#     except Catagoriesofitems.DoesNotExist:
#         # 4. Not a category—maybe it’s a subcategory?
#         sub_objs = SubCatagoriesofitems.objects.filter(subCatagory_name=name)

#         # cards under this subcategory
#         card_qs = CardDetails.objects.filter(subcategory=sub_objs)
#         # to keep your template loop happy, re‑use the parent category’s subcats
#         subcata_qs = SubCatagoriesofitems.objects.filter(category=sub_objs.category)

#     # 5. Apply any sorting
#     if sort_option == 'name_asc':
#         card_qs = card_qs.order_by('cardtitle')
#     elif sort_option == 'name_desc':
#         card_qs = card_qs.order_by('-cardtitle')
#     elif sort_option == 'price_asc':
#         card_qs = card_qs.order_by('price')
#     elif sort_option == 'price_desc':
#         card_qs = card_qs.order_by('-price')
#     elif sort_option == 'rating_desc':
#         card_qs = card_qs.order_by('-rating')

#     # 6. Render
#     return render(request, "DynamicPage/Dynamic.html", {
#         'catagories':   catagories,
#         'cards':        card_qs,
#         'pagename':     pagename,
#         'selected_sort': sort_option,
#         'subcata':      subcata_qs,
#     })


def DynamicForSubcategory(request, name):
    # Fetch all categories for the template
    categories = Catagoriesofitems.objects.all()
    pagename = name
    card_qs = CardDetails.objects.none()
    subcategory_qs = SubCatagoriesofitems.objects.none()
    sort_option = request.GET.get('sort')

    try:
        # Try to fetch the first matching subcategory (avoid .get())
        subcata = SubCatagoriesofitems.objects.filter(subCatagory_name=name).first()
        if subcata:
            # Subcategory match
            card_qs = CardDetails.objects.filter(subcategory=subcata)
            # Fetch other subcategories under the same category as the matched subcategory
            subcategory_qs = SubCatagoriesofitems.objects.filter(category=subcata.category)
        else:
            # No subcategory match → check if it's a category
            cat_objs = Catagoriesofitems.objects.filter(Catagory_name=name)
            if cat_objs.exists():
                # Fetch cards that belong to this category
                card_qs = CardDetails.objects.filter(category__in=cat_objs)

                # This line assumes all categories have the same subcategories
                # Safe only if all cat_objs share the same subcategory
                first_cat = cat_objs.first()
                subcategory_qs = SubCatagoriesofitems.objects.filter(category=first_cat)

    except Exception as e:
        print("Unexpected error:", e)

    # Sorting logic
    if sort_option == 'name_asc':
        card_qs = card_qs.order_by('cardtitle')
    elif sort_option == 'name_desc':
        card_qs = card_qs.order_by('-cardtitle')
    elif sort_option == 'price_asc':
        card_qs = card_qs.order_by('price')
    elif sort_option == 'price_desc':
        card_qs = card_qs.order_by('-price')
    elif sort_option == 'rating_desc':
        card_qs = card_qs.order_by('-rating')

    # Render the page with the appropriate context
    return render(request, "DynamicPage/Dynamic.html", {
        'catagories': categories,
        'cards': card_qs,
        'pagename': pagename,
        'selected_sort': sort_option,
        'subcategories': subcategory_qs,
    })



def Dynamic(request, name):
    catagories = Catagoriesofitems.objects.all()
    pagename = name
    card_qs = CardDetails.objects.none()
    subcata_qs = SubCatagoriesofitems.objects.none()
    sort_option = request.GET.get('sort')

    try:
        # Try to fetch the first matching category (avoid .get())
        cata = Catagoriesofitems.objects.filter(Catagory_name=name).first()
        if cata:
            # Category match
            card_qs = CardDetails.objects.filter(category=cata)
            subcata_qs = SubCatagoriesofitems.objects.filter(category=cata)
        else:
            # No category match → check if it's a subcategory
            sub_objs = SubCatagoriesofitems.objects.filter(subCatagory_name=name)
            if sub_objs.exists():
                card_qs = CardDetails.objects.filter(subcategory__in=sub_objs)

                # This line assumes all subcategories have the same category
                # Safe only if all sub_objs share the same category
                first_sub = sub_objs.first()
                subcata_qs = SubCatagoriesofitems.objects.filter(category=first_sub.category)

    except Exception as e:
        print("Unexpected error:", e)

    # Sorting logic
    if sort_option == 'name_asc':
        card_qs = card_qs.order_by('cardtitle')
    elif sort_option == 'name_desc':
        card_qs = card_qs.order_by('-cardtitle')
    elif sort_option == 'price_asc':
        card_qs = card_qs.order_by('price')
    elif sort_option == 'price_desc':
        card_qs = card_qs.order_by('-price')
    elif sort_option == 'rating_desc':
        card_qs = card_qs.order_by('-rating')

    return render(request, "DynamicPage/Dynamic.html", {
        'catagories': catagories,
        'cards': card_qs,
        'pagename': pagename,
        'selected_sort': sort_option,
        'subcata': subcata_qs,
    })


model_map = {
    "All offers": OffersSection,
    "You can purchase": Recomendations,
    "Growth Promoters": GrowthSection,
    "Smart farmer's needs": SmartfarmingSection,
    "Sprays": SpraySection,
    "Seeds": SeedsSection,
    "Seasonal collections": SeasonalSection,
    
}

# Dynamic Page based on section name
# def sectionDynamic(request, name):
#     try:
#         model_class = model_map.get(name)
#         if model_class is None:
#             return HttpResponse("Invalid section", status=404)
        
#         catagories = Catagoriesofitems.objects.all()
#         pagename = name
#         pagesection = model_class.objects.all()

#         product_names = [item.productname for item in pagesection]
#         card = CardDetails.objects.filter(cardtitle__in=product_names).distinct()

#         # Get sort option from URL
#         sort_option = request.GET.get('sort')

#         # Apply sorting
#         if sort_option == 'name_asc':
#             card = card.order_by('cardtitle')
#         elif sort_option == 'name_desc':
#             card = card.order_by('-cardtitle')
#         elif sort_option == 'price_asc':
#             card = card.order_by('price')
#         elif sort_option == 'price_desc':
#             card = card.order_by('-price')
#         elif sort_option == 'rating_desc':
#             card = card.order_by('-rating')

#     except CardDetails.DoesNotExist:
#         return HttpResponse("Category not found", status=404)

#     return render(request, "DynamicPage/Dynamic.html", {
#         'catagories': catagories,
#         'cards': card,
#         'pagename': pagename,
#         'is_string': True,
#         'selected_sort': sort_option,
#     })
def sectionDynamic(request, name):
    try:
        model_class = model_map.get(name)
        if model_class is None:
            return HttpResponse("Invalid section", status=404)
        
        catagories = Catagoriesofitems.objects.all()
        pagename = name
        pagesection = model_class.objects.all()

        # Unique product names
        product_names = list(dict.fromkeys(item.productname for item in pagesection))

        # Fetch one unique CardDetails entry per product
        card_ids = (CardDetails.objects
                    .filter(cardtitle__in=product_names)
                    .values('cardtitle')
                    .annotate(min_id=Min('id'))
                    .values_list('min_id', flat=True))
        
        card = CardDetails.objects.filter(id__in=card_ids)

        # Sorting
        sort_option = request.GET.get('sort')
        if sort_option == 'name_asc':
            card = card.order_by('cardtitle')
        elif sort_option == 'name_desc':
            card = card.order_by('-cardtitle')
        elif sort_option == 'price_asc':
            card = card.order_by('price')
        elif sort_option == 'price_desc':
            card = card.order_by('-price')
        elif sort_option == 'rating_desc':
            card = card.order_by('-rating')

    except CardDetails.DoesNotExist:
        return HttpResponse("Category not found", status=404)

    return render(request, "DynamicPage/Dynamic.html", {
        'catagories': catagories,
        'cards': card,
        'pagename': pagename,
        'is_string': True,
        'selected_sort': sort_option,
    })



# Register
def Signup(request):
    if request.user.is_authenticated:
        return redirect('/home/')

    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        phone=request.POST.get('phone')
        # Password validation
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('/signup/')

        # Username validation
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('/signup/')

        # Email validation
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('/signup/')

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password1,
                                        first_name=first_name, last_name=last_name)
        
        user.save()

        # Create user profile (you can add additional fields like phone, address, etc. if needed)
        user_profile = UserProfile(user=user,phone=phone)
        user_profile.save()

        # Provide feedback to the user
        messages.success(request, "Account created successfully.")
        return redirect('/signin/')

    return render(request, "auth/Signup.html")

# Login
def Signin(request):
    
    if request.user.is_authenticated:
        return redirect('/home/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect('/home/')
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('/signin/')

    return render(request, "auth/Signin.html")

# Logout
def logout(request):
    if not request.user.is_superuser:
        auth_logout(request)
        messages.success(request, "You have been logged out.")
        return redirect('/signin/')
    else:
        auth_logout(request)
        messages.success(request, "You have been logged out.")
        return redirect('/signin/')



# product view
def productview(request,id):
    catagories = Catagoriesofitems.objects.all()
    product=CardDetails.objects.get(id=id)
    return render(request,'productdiscription.html',{"catagories":catagories,"product":product})



@login_required
def cartview(request):
    catagories = Catagoriesofitems.objects.all()
    
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    all_order_items = OrderItem.objects.filter(order__in=orders,is_ordered=False).select_related('product')
    cards = CardDetails.objects.all()
    for card in cards:
        card.final_price = card.discounted_price
    CardDetails.objects.bulk_update(cards, ['final_price'])

    order_items_map = defaultdict(list)
    for item in all_order_items:
        order_items_map[item.order].append(item)
    
    orders_with_items = []
    grand_total = Decimal('0.00')
    product_count = 0
    all_product_names = []
    cart_product_ids = []  # collect product IDs

    for order in orders:
        items = order_items_map[order]
        total = sum(item.price * item.quantity for item in items)
        grand_total += total
        product_count += sum(item.quantity for item in items)
        all_product_names.extend(item.product.cardtitle for item in items)
        cart_product_ids.extend(item.product.id for item in items)  # collect product IDs

        orders_with_items.append({
            'order': order,
            'items': items,
            'total': total,
        })

    unique_product_count = len(set(all_product_names))

    # Save cart product IDs in session
    request.session['cart_product_ids'] = list(set(cart_product_ids))  # remove duplicates if needed

    return render(request, 'cart.html', {
        'catagories': catagories,
        'orders_with_items': orders_with_items,
        'grand_total': grand_total,
        'product_count': product_count,
        'unique_product_count': unique_product_count,
    })


@login_required
@transaction.atomic
def request_for_deal(request, id):
    if request.method == 'POST':
        product = get_object_or_404(CardDetails, id=id)
        quantity = int(request.POST.get('quantity', 1))
        price = product.final_price
        # Get all unpaid orders for the user
        orders = Order.objects.filter(user=request.user, is_paid=False)

        # If no unpaid orders exist, create a new one
        if not orders.exists():
            order = Order.objects.create(user=request.user, is_paid=False, total_price=Decimal('0.00'))
        else:
            order = orders.first()  # You can select the first unpaid order or apply custom logic

        # Check if product already in order -> update quantity
        order_item, item_created = OrderItem.objects.get_or_create(
            order=order,
            product=product,
            defaults={'quantity': quantity, 'price': price}
        )
        if not item_created:
            order_item.quantity += quantity
            order_item.save()
        product.max_product -= quantity  # Decrease available stock
        product.save()
        product.refresh_from_db()
        # Recalculate total_price
        total = sum(item.price * item.quantity for item in order.orderitem_set.all())
        order.total_price = total
        order.save()

    return redirect('/cart/')

@require_POST
@login_required
@transaction.atomic
def updateorders(request, action, value):
    try:
        # Ensure value is an integer (value comes from URL as str or int depending on URLConf)
        try:
            value = int(value)
        except ValueError:
            messages.error(request, "Invalid quantity value.")
            return redirect('/cart/')

        # Get the product ID from the POST request
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(CardDetails, id=product_id)

        # Find the active unpaid order for the user
        order = Order.objects.filter(user=request.user, is_paid=False).first()

        if not order:
            messages.error(request, "No active order found.")
            return redirect('/cart/')

        # Get the order item related to the product
        order_item = OrderItem.objects.get(order=order, product=product)

        # Perform the action (Add/Subtract/Delete quantity)
        if action == "Add":
            if value > product.max_product:
                messages.error(request, f"You can't add more than {product.max_product} items for this product.")
                return redirect('/cart/')

            order_item.quantity += value
            product.max_product-= value  # Decrease available stock
            if product.max_product < 0:
                product.max_product = 0
            product.save()
            product.refresh_from_db() 
            

        elif action == "Sub":
            
            if value >= order_item.quantity:
                product.max_product += order_item.quantity
                order_item.delete()
                messages.success(request, "Item removed from your order.")
            else:
                order_item.quantity -= value
                
                order_item.save()
            product.save()
            product.refresh_from_db() 
            # Recalculate total price after update
            total = sum(item.price * item.quantity for item in order.orderitem_set.all())
            order.total_price = total
            order.save()

            return redirect('/cart/')

        elif action == "Remove":
            product.max_product+= order_item.quantity
            order_item.delete()
            product.save()
            product.refresh_from_db() 
            messages.success(request, "Item removed from your order.")

            # Recalculate total price after item removal
            total = sum(item.price * item.quantity for item in order.orderitem_set.all())
            order.total_price = total
            order.save()

            return redirect('/cart/')

        # For Add action, we still need to save order_item and recalculate
        order_item.save()
        total = sum(item.price * item.quantity for item in order.orderitem_set.all())
        order.total_price = total
        order.save()

        return redirect('/cart/')

    except OrderItem.DoesNotExist:
        messages.error(request, "Item not found in your order.")
        return redirect('/cart/')

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        messages.error(request, "Something went wrong.")
        return redirect('/cart/')





def farmer(request):
    catagories = Catagoriesofitems.objects.all()
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        brand = request.POST.get('brand')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')
        category = request.POST.get('category')
        additional_info = request.POST.get('additional_info')

        if request.user.is_authenticated:
            logout(request)

        existing_users = User.objects.filter(email=email)

        # Check all existing users for a matching profile
        for existing_user in existing_users:
            try:
                seller_profile = SellerProfile.objects.get(user=existing_user)
                if seller_profile.name == name and seller_profile.contact == contact and seller_profile.brand == brand \
                    and seller_profile.address == address and seller_profile.city == city and seller_profile.state == state \
                    and seller_profile.zip == zip_code and seller_profile.category == category and seller_profile.additional_info == additional_info:
                    
                    user = authenticate(request, username=existing_user.username, password='sellerpassword123')
                    if user:
                        auth_login(request, user)
                        return redirect('far_dash')
            except SellerProfile.DoesNotExist:
                continue

        # If no matching seller found, create a new user and seller
        user = User.objects.create_user(username=email + str(User.objects.filter(email=email).count()), email=email, password='sellerpassword123')
        user.save()

        seller = SellerProfile.objects.create(
            user=user,
            name=name,
            email=email,
            contact=contact,
            brand=brand,
            address=address,
            city=city,
            state=state,
            zip=zip_code,
            category=category,
            additional_info=additional_info
        )

        user = authenticate(request, username=user.username, password='sellerpassword123')
        if user:
            auth_login(request, user)
            return redirect('far_dash')

    return render(request, 'sell/farmers.html',{'catagories': catagories,})

def far_dash(request):
    catagories = Catagoriesofitems.objects.all()
    subcategories = SubCatagoriesofitems.objects.all()
    products = ProductsOfthisWeb.objects.filter(added_by=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully.")
            return redirect('far_dash')
        else:
            messages.error(request, "Form submission failed. Please check your input.")
            return redirect(request.path)

    return render(request, 'sell/farmersdashboard.html', {
        'catagories': catagories,
        'subcategories': subcategories,
        'products': products,
    })


    # return render(request, "sell/farmersdashboard.html", {
    #     'catagories': catagories,
    #     'subcategories': subcategories,
    #     'products': products
    # })




def update_product(request, pk):
    product = get_object_or_404(ProductsOfthisWeb, id=pk)
    
    if request.method == 'POST':
        # Handle image fields safely from request.FILES
        if 'image' in request.FILES:
            product.image = request.FILES['image']
        if 'image1' in request.FILES:
            product.image1 = request.FILES['image1']
        if 'image2' in request.FILES:
            product.image2 = request.FILES['image2']
        if 'image3' in request.FILES:
            product.image3 = request.FILES['image3']

        # Other fields from request.POST
        product.product_name = request.POST.get('product_name', product.product_name)
        product.price = request.POST.get('price', product.price)
        value = request.POST.get('max_product', product.max_product)

        try:
            product.max_product = int(value)
        except ValueError:
            pass  # Or you can handle this with a message

        product.unit_of_measurement = request.POST.get('unit_of_measurement', product.unit_of_measurement)
        product.Description = request.POST.get('Description', product.Description)

        # Save the updated product
        product.save()
        return redirect('far_dash')

def delete_product(request, pk):
    product = get_object_or_404(ProductsOfthisWeb, id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('far_dash')
    
def search(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        words = query.strip().split()
        qs = CardDetails.objects.all()
        
        for word in words:
            qs = qs.filter(
                Q(cardtitle__icontains=word) |
                Q(Description__icontains=word) |
                Q(Description_of_product__icontains=word)
            )
        
        if qs.exists():
            for card in qs:
                results.append({
                    'id': card.id,
                    'title': card.cardtitle,
                    'price': float(card.price),
                    'image': card.image.url if card.image else '',
                    'availablity': card.availablity,
                    'discounted_price': float(card.discounted_price),
                })
            return JsonResponse({'results': results, 'status': 'success'})
        else:
            return JsonResponse({'results': [], 'status': 'not_found', 'message': 'No products matched your search.'})
    
    return JsonResponse({'results': [], 'status': 'empty_query', 'message': 'Please enter a search term.'})


@login_required
def download_receipt_pdf(request):
    user = request.user

    # Step 1: Get the latest order by order_id
    latest_order = orderplacedfinal.objects.filter(user_username=user.username).order_by('-created_at').first()
    if not latest_order:
        return HttpResponse("No orders found.", status=404)

    order_id = latest_order.order_id

    # Step 2: Fetch all items for that order_id
    latest_orders = orderplacedfinal.objects.filter(user_username=user.username, order_id=order_id)

    # Step 3: Calculate totals
    subtotal = sum(item.Price * item.quantity for item in latest_orders)
    discount = Decimal('0.00')
    total = subtotal - discount

    # Step 4: Render HTML template to string
    html = render_to_string('receipt_template.html', {
        'username': user.username,
        'order_date': latest_order.created_at,
        'orders': latest_orders,
        'subtotal': subtotal,
        'discount': discount,
        'total': total,
    })

    # Step 5: Create PDF
    result = BytesIO()
    pdf = pisa.CreatePDF(BytesIO(html.encode("utf-8")), dest=result)
    if pdf.err:
        return HttpResponse("Error generating PDF", status=500)

    # Step 6: Return as downloadable file
    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="AgriShop_Receipt.pdf"'
    return response

        
def check(request):
    return render(request,'order_confirmation.html')



@login_required
def placeorderone(request, id):
    product = get_object_or_404(CardDetails, id=id)

    if request.method == "POST":
        # Fetching form data
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')
        quantity = int(request.POST.get('quantity', 1))  # Get quantity from the form (default is 1)

        # Basic form validation
        if not address or not city or not state or not zip_code:
            messages.error(request, "All address fields are required.")
            return redirect('placeorderone', id=id)

        if quantity <= 0:
            messages.error(request, "Quantity must be greater than zero.")
            return redirect('placeorderone', id=id)

        # Check if the quantity exceeds available stock
        if product.max_product < quantity:
            messages.error(request, f"Only {product.max_product} items are available.")
            return redirect('placeorderone', id=id)

        # Save address to user profile
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile.Address = address
        profile.City = city
        profile.State = state
        profile.Zip = zip_code
        profile.save()

        total_price = product.price * Decimal(quantity)

        # # Create order
        # order = Order.objects.create(
        #     user=request.user,
        #     total_price=total_price,
        #     product_count=quantity,
        # )

        # # Add item to order
        # OrderItem.objects.create(
        #     order=order,
        #     product=product,
        #     quantity=quantity,
        #     price=product.price,
        #     is_ordered=True,
        # )
        orderplaced=OrderItem.objects.filter(order__user=request.user,product=product).first()
        cratedate=Order.objects.filter(user=request.user,orderitem__product=product).first()
        theorders=orderplacedfinal.objects.create(
            user_username=request.user.username,
            user_other_details=f"Address: {address}, City: {city}, State: {state}, Zip: {zip_code}",
            product_name=product.cardtitle,
            quantity=orderplaced.quantity,
            Price=orderplaced.price,
            created_at=cratedate.created_at
        )
        theorders.save()
        cratedate.delete()
        orderplaced.delete()
        # Update max_product based on the ordered quantity
        product.max_product -= quantity
        product.save()

        messages.success(request, "Order placed successfully!")
        return redirect('/check/')  # or replace with your summary page

    return render(request, 'buynow.html', {'product': product})

@login_required
def placeorderall(request):
    user = request.user
    success = False
    try:
    
        if request.method == "POST":
                address = request.POST.get('address')
                city = request.POST.get('city')
                state = request.POST.get('state')
                zip_code = request.POST.get('zip')

                if not address or not city or not state or not zip_code:
                    messages.error(request, "All address fields are required.")
                    return redirect('placeorderall')  # Or however you route to this view

                # Save address to user profile
                user_profile, created = UserProfile.objects.get_or_create(user=user)
                user_profile.Address = address
                user_profile.City = city
                user_profile.State = state
                user_profile.Zip = zip_code
                user_profile.save()

                    # Get current user's active order
                order = Order.objects.filter(user=user).first()

                if not order:
                    messages.warning(request, "No items to place an order.")
                    return redirect('cart_view')  # or some fallback page

                order_items = OrderItem.objects.filter(order=order)
                    
                    
                    # Get user profile details
                user_profile = UserProfile.objects.filter(user=user).first()
                user_other_details = f"{user_profile.Address}, {user_profile.City}, {user_profile.State}, {user_profile.Zip}" if user_profile else "Not Provided"
                shared_order_id = uuid.uuid4()
                for item in order_items:
                        # Save to orderplacedfinal
                    orderplacedfinal.objects.create(
                        order_id=shared_order_id,
                        user_username=user.username,
                        user_other_details=user_other_details,
                        product_name=item.product.cardtitle,
                        Price=item.price,
                        quantity=item.quantity,
                    )

                    # Save cart_items and total_amount before deleting
                cart_items = list(order_items)  # Make a copy
                total_amount = sum(item.price for item in cart_items)

                    # Delete all related OrderItems and the Order itself
                order_items.delete()
                order.delete()

                messages.success(request, "Your order has been placed successfully!")
                return redirect('/check/')
                
            
        return render(request, 'buynow.html', {
            
            
            'states': [
                'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
                'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka',
                'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya',
                'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim',
                'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand',
                'West Bengal', 'Dhaka', 'Khulna', 'Rajshahi', 'Chattogram',
                'Sindh', 'Khyber Pakhtunkhwa', 'Balochistan', 'Province 1', 'Province 2',
                'Bagmati', 'Gandaki', 'Lumbini', 'Karnali', 'Sudurpashchim'
            ],
        })

    except Exception as e:
        print("Error placing order:", e)
        messages.error(request, "There was an error processing your order.")
        return redirect('cart_view')  # Or wherever appropriate
    
    
@login_required
def profile_editing(request):
    if request.method == 'POST':
        user = request.user
        profile = user.userprofile

        user.first_name = request.POST.get('firstname')
        user.last_name = request.POST.get('lastname')
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()

        profile.phone = request.POST.get('phone')
        profile.save()

        messages.success(request, "Profile updated successfully.")
        return redirect('profile_editing')

    return render(request, 'editprofile.html', {'user': request.user})





# class CustomPasswordResetView(PasswordResetView):
#     def send_mail(self, subject_template_name, email_template_name,
#                   context, from_email, to_email, html_email_template_name=None):
#         subject = render_to_string(subject_template_name, context).strip()
#         text_body = render_to_string(email_template_name, context)
#         html_body = render_to_string('registration/password_reset_email.html', context)

#         email = EmailMultiAlternatives(subject, text_body, from_email, [to_email])
#         email.attach_alternative(html_body, "text/html")
#         email.send()



class CustomPasswordResetView(PasswordResetView):
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):

        request = self.request
        current_site = get_current_site(request)

        context['protocol'] = 'https' if request.is_secure() else 'http'
        context['domain'] = current_site.domain

        subject = render_to_string(subject_template_name, context).strip()
        text_body = render_to_string(email_template_name, context)
        html_body = render_to_string(html_email_template_name or 'registration/password_reset_email.html', context)

        email = EmailMultiAlternatives(subject, text_body, from_email, [to_email])
        email.attach_alternative(html_body, "text/html")
        email.send()

