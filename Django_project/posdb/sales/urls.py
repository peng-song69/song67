# sales/urls.py (កូដដែលកែសម្រួលរួចរាល់)

# sales/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # ── Part 1 & 2 views ──────────────────────────────────────
    path('products/',             views.product_list,   name='product_list'),
    path('products/<int:pk>/',     views.product_detail, name='product_detail'),
    path('orders/',                views.order_list,     name='order_list'),
    path('orders/new/',            views.create_order,   name='create_order'),
    path('orders/<int:pk>/items/', views.add_item,       name='add_item'),

    # ── HW3: My Orders ───────────────────────────────────────
    path('orders/mine/',           views.my_orders,      name='my_orders'),

    # ── HW5: Cancel Order (ថ្មី) ──────────────────────────────
    path('orders/<int:pk>/cancel/', views.cancel_order,  name='cancel_order'),
]