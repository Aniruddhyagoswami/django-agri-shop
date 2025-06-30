from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name='home'),  # Home page
    path('home/', home, name='home'),  # Redundant but may be kept for SEO purposes
    path('aboutus/', aboutus, name='aboutus'),  # About us page
    path('contact/', Contact, name='contact'),  # Contact page
    path('findDynamic/<str:name>/', Dynamic, name='find_dynamic'),  # Dynamic Pages
    path('Dynamic/<str:name>/', sectionDynamic, name='section_dynamic'),  # Dynamic Pages
    path('subcategory/<str:name>/', DynamicForSubcategory, name='dynamic_subcategory'), # Dynamic Pages
    path('signin/', Signin, name='signin'),  # Signin page
    path('signup/', Signup, name='signup'),  # Signup page
    path('logout/', logout, name='logout'),  # Logout page
    path('summernote/', include('django_summernote.urls')),  # Summernote integration for text editing
    path('sell/',farmer,name='farmer'),
    path('productview/<int:id>',productview,name='productview'),  # Product view page
    
    path('search/',search,name='search'),
    # cart system
    path('cart/', cartview, name='cart_view'),
    path('cart/add/<int:id>', request_for_deal),
    path('download/',download_receipt_pdf,name='download_receipt_pdf'),
    path('cart/add/<int:id>/', request_for_deal, name='cart_add'),
    path('check/',check),
    # ✅ This is the main path to update quantity dynamically
    path('updateorders/<str:action>/<int:value>/', updateorders, name='updateorders'),
    path('farmerdash/',far_dash,name='far_dash'),
    path('delete-product/<int:product_id>/', delete_product, name='delete_product'),
    path('buynow/<int:id>',placeorderone,name='placeorderone'),
    path('buynow/',placeorderall,name='placeorderall'),
    path('product/update/<int:pk>/', update_product, name='update_product'),
    path('product/delete/<int:pk>/', delete_product, name='delete_product'),
    path('edit-profile/',profile_editing, name='profile_editing'),
    
    # password reset
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    #  path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/',  CustomPasswordResetView.as_view(
    template_name='registration/password_reset_form.html',
    email_template_name='registration/password_reset_email.txt',
    subject_template_name='registration/password_reset_subject.txt',
    html_email_template_name='registration/password_reset_email.html'  # 👈 REQUIRED!
    ), name='password_reset'),
    ]
