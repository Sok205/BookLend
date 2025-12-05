from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Count, Sum, F, Value, CharField
from django.db.models.functions import Concat

from .models import Book, Loan, Borrower, Customer, Item, OrderInfo, OrderLine, Stock, Barcode
from .forms import BorrowerForm, LoanForm, BorrowerSearchForm, BookForm


def index(request):
    return render(request, 'catalog/index.html')


def loans_list(request):
    loans = Loan.objects.select_related('book', 'borrower').all()
    return render(request, 'catalog/loans_list.html', {'loans': loans})


def borrower_search(request):
    form = BorrowerSearchForm(request.GET or None)
    results = None
    name = ''
    if form.is_valid():
        name = form.cleaned_data['family_name']
        results = Loan.objects.select_related('book', 'borrower').filter(borrower__family_name__icontains=name)
    return render(request, 'catalog/borrower_search.html', {'form': form, 'results': results, 'name': name})


def books_borrow_count(request):
    books = Book.objects.annotate(times_borrowed=Count('loans')).order_by('-times_borrowed')
    return render(request, 'catalog/books_borrow_count.html', {'books': books})


def add_borrower(request):
    if request.method == 'POST':
        form = BorrowerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('catalog:index'))
    else:
        form = BorrowerForm()
    return render(request, 'catalog/add_borrower.html', {'form': form})


def add_loan(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('catalog:loans_list'))
    else:
        form = LoanForm()
    return render(request, 'catalog/add_loan.html', {'form': form})


def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('catalog:index'))
    else:
        form = BookForm()
    return render(request, 'catalog/add_book.html', {'form': form})


def all_books(request):
    books = Book.objects.all()
    return render(request, 'catalog/books_list.html', {'books': books})


def all_borrowers(request):
    borrowers = Borrower.objects.all()
    return render(request, 'catalog/borrowers_list.html', {'borrowers': borrowers})


def all_customers(request):
    customers = Customer.objects.all()
    return render(request, 'catalog/customers_list.html', {'customers': customers})


def all_items(request):
    items = Item.objects.all()
    return render(request, 'catalog/items_list.html', {'items': items})


def all_orders(request):
    orders = OrderInfo.objects.select_related('customer').all()
    return render(request, 'catalog/orders_list.html', {'orders': orders})


def all_stock(request):
    stock = Stock.objects.select_related('item').all()
    return render(request, 'catalog/stock_list.html', {'stock': stock})


def all_orderlines(request):
    orderlines = OrderLine.objects.select_related('orderinfo', 'item').all()
    return render(request, 'catalog/orderlines_list.html', {'orderlines': orderlines})


def all_barcodes(request):
    barcodes = Barcode.objects.select_related('item').all()
    return render(request, 'catalog/barcodes_list.html', {'barcodes': barcodes})

def query1_customers_town_h(request):
    """Query 1: Customers from towns starting with 'h'"""
    customers = Customer.objects.filter(town__istartswith='h')
    return render(request, 'catalog/query1.html', {'customers': customers})


def query2_items_null(request):
    """Query 2: Items with NULL cost_price or sell_price"""
    from django.db.models import Q
    items = Item.objects.filter(Q(cost_price__isnull=True) | Q(sell_price__isnull=True))
    return render(request, 'catalog/query2.html', {'items': items})


def query3_customers_separate(request):
    """Query 3: All customers with columns shown separately"""
    customers = Customer.objects.all()
    return render(request, 'catalog/query3.html', {'customers': customers})


def query4_customers_concat(request):
    """Query 4: All customers concatenated into one string"""
    customers = Customer.objects.annotate(
        customer_info=Concat(
            'id', Value(' '),
            'title', Value(' '),
            'fname', Value(' '),
            'lname', Value(' '),
            'addressline', Value(' '),
            'town', Value(' '),
            'zipcode', Value(' '),
            'phone',
            output_field=CharField()
        )
    )
    return render(request, 'catalog/query4.html', {'customers': customers})


def query5_order_details(request):
    """Query 5: All order details with items"""
    order_details = OrderLine.objects.select_related(
        'orderinfo__customer', 'item'
    ).values(
        'orderinfo__id',
        'orderinfo__customer__fname',
        'orderinfo__customer__lname',
        'orderinfo__date_placed',
        'item__description',
        'quantity'
    ).order_by('orderinfo__id')
    return render(request, 'catalog/query5.html', {'order_details': order_details})


def query6_order_totals(request):
    """Query 6: Order totals (without shipping)"""
    order_totals = OrderLine.objects.select_related(
        'orderinfo__customer', 'item'
    ).values(
        'orderinfo__id',
        'orderinfo__customer__fname',
        'orderinfo__customer__lname',
        'orderinfo__date_placed'
    ).annotate(
        total_value=Sum(F('quantity') * F('item__sell_price'))
    ).order_by('orderinfo__id')
    return render(request, 'catalog/query6.html', {'order_totals': order_totals})


def query7_ann_stones_orders(request):
    """Query 7: Items ordered by Ann Stones"""
    ann_orders = OrderLine.objects.select_related(
        'orderinfo__customer', 'item'
    ).filter(
        orderinfo__customer__fname='Ann',
        orderinfo__customer__lname='Stones'
    ).values(
        'orderinfo__id',
        'orderinfo__customer__fname',
        'orderinfo__customer__lname',
        'orderinfo__date_placed',
        'item__description',
        'quantity'
    ).order_by('orderinfo__id')
    return render(request, 'catalog/query7.html', {'ann_orders': ann_orders})
