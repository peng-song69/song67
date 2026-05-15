# sales/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem
from .forms import OrderItemForm

@login_required
def product_list(request):
    """បង្ហាញផលិតផល active ទាំងអស់ តម្រៀប A–Z"""
    products = Product.objects.filter(is_active=True)
    return render(request, 'sales/product_list.html', {'products': products})

@login_required
def product_detail(request, pk):
    """បង្ហាញព័ត៌មានលម្អិតសម្រាប់ផលិតផលតែមួយ។ Return 404 ប្រសិនបើរកមិនឃើញ"""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'sales/product_detail.html', {'product': product})

@login_required
def order_list(request):
    """បង្ហាញការបញ្ជាទិញទាំងអស់ ថ្មីបំផុតមុន"""
    orders = Order.objects.all()
    return render(request, 'sales/order_list.html', {'orders': orders})

@login_required
def create_order(request):
    """Instantly create an open order and jump straight to the add-items page."""
    order = Order.objects.create(
        cashier=request.user,
        status='open',
    )
    return redirect('add_item', pk=order.pk)


@login_required
def add_item(request, pk):
    """
    អនុញ្ញាតឱ្យអ្នកគិតលុយបន្ថែមទំនិញ កាត់ស្តុក និងប្តូរស្ថានភាពទៅជា Pai
    """
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        # ប៊ូតុង "Mark as Paid"
        if 'mark_paid' in request.POST:
            order.status = 'paid'
            order.save()
            return redirect('order_list')

        # បញ្ចូលទំនិញថ្មី
        item_form = OrderItemForm(request.POST)
        if item_form.is_valid():
            item = item_form.save(commit=False)
            item.order      = order
            item.unit_price = item.product.price   # រក្សាតម្លៃទុក
            item.save()

            # --- ផ្នែកកាត់ស្តុក (HW 4) ---
            product = item.product         # ទាញយកផលិតផល
            product.stock -= item.quantity # ដកចំនួនដែលលក់ចេញពីស្តុក
            product.save()                 # រក្សាទុកការផ្លាស់ប្តូរចូល Database
            # --------------------------

            return redirect('add_item', pk=order.pk)
    else:
        item_form = OrderItemForm()

    return render(request, 'sales/add_item.html', {
        'order':     order,
        'item_form': item_form,
        'items':     order.items.select_related('product'),
    })
@login_required
def my_orders(request):
    """បង្ហាញតែការលក់របស់បុគ្គលិកដែលកំពុងប្រើប្រាស់ (ភារកិច្ច ៣)"""
    # ទាញយក Order ណាដែលមាន cashier ស្មើនឹង User ដែលបាន Login
    orders = Order.objects.filter(cashier=request.user)
    
    return render(request, 'sales/order_list.html', {
        'orders': orders,
        'title': 'ការលក់របស់ខ្ញុំ (My Orders)'
    })

@login_required
def cancel_order(request, pk):
    """បោះបង់ការលក់ និងបូកស្តុកត្រឡប់ទៅវិញ (ភារកិច្ច ៥)"""
    order = get_object_or_404(Order, pk=pk)
    
    # យើងអនុញ្ញាតឱ្យ Cancel តែ Order ណាដែលមិនទាន់ Cancel ប៉ុណ្ណោះ
    if order.status != 'cancelled':
        # ១. បូកស្តុកត្រឡប់ទៅវិញសម្រាប់រាល់ទំនិញក្នុង Order នេះ
        for item in order.items.all():
            product = item.product
            product.stock += item.quantity # បូកបញ្ជូលក្នុងស្តុកវិញ
            product.save()
        
        # ២. ប្តូរស្ថានភាព Order ទៅជា Cancelled
        order.status = 'cancelled'
        order.save()
        
    return redirect('order_list')