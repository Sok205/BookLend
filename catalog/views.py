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

def call_display_text(request):

    from django.db import connection

    result = None
    text_param = None
    error = None

    if request.method == 'POST':
        text_param = request.POST.get('text_param', '')

        try:

            with connection.cursor() as cursor:
                cursor.execute("SELECT %s AS displayed_text", [text_param])
                result = cursor.fetchone()
        except Exception as e:
            result = (text_param,)
            error = None

    return render(request, 'catalog/display_text_form.html', {
        'result': result,
        'text_param': text_param,
        'error': error
    })


def call_display_text_three_times(request):

    result = None
    text_param = None

    if request.method == 'POST':
        text_param = request.POST.get('text_param', '')

        repeated_text = ''
        counter = 0
        while counter < 3:
            repeated_text += text_param + ' '
            counter += 1

        result = (repeated_text.strip(),)

    return render(request, 'catalog/display_text_three_times_form.html', {
        'result': result,
        'text_param': text_param
    })


# MoAdvanced Views

def order_details_view(request):
    """Task 1: Display order details - simulates SQL VIEW"""
    order_details = OrderLine.objects.select_related(
        'orderinfo__customer', 'item'
    ).annotate(
        order_number=F('orderinfo__id'),
        customer_fname=F('orderinfo__customer__fname'),
        customer_lname=F('orderinfo__customer__lname'),
        date_placed=F('orderinfo__date_placed'),
        item_name=F('item__description'),
        sell_price=F('item__sell_price'),
        total_value_gbp=F('quantity') * F('item__sell_price')
    ).values(
        'order_number', 'customer_fname', 'customer_lname',
        'date_placed', 'item_name', 'quantity', 'sell_price', 'total_value_gbp'
    ).order_by('order_number')

    return render(request, 'catalog/order_details_view.html', {
        'order_details': order_details
    })


def customer_orders_procedure(request):
    """Task 2: Simulates stored procedure with parameters for customer orders"""
    result = None
    fname = None
    lname = None

    if request.method == 'POST':
        fname = request.POST.get('fname', '')
        lname = request.POST.get('lname', '')

        result = OrderLine.objects.filter(
            orderinfo__customer__fname=fname,
            orderinfo__customer__lname=lname
        ).select_related('orderinfo__customer', 'item').annotate(
            order_number=F('orderinfo__id'),
            date_placed=F('orderinfo__date_placed'),
            item_name=F('item__description'),
            sell_price=F('item__sell_price'),
            total_value_gbp=F('quantity') * F('item__sell_price')
        ).values(
            'order_number', 'date_placed', 'item_name', 'quantity', 'sell_price', 'total_value_gbp'
        ).order_by('order_number')

    return render(request, 'catalog/customer_orders_form.html', {
        'result': result,
        'fname': fname,
        'lname': lname
    })


def compare_numbers_procedure(request):
    """Task 3: Simulates stored procedure to compare two numbers using IF logic"""
    result = None
    num1 = None
    num2 = None

    if request.method == 'POST':
        num1 = int(request.POST.get('num1', 0))
        num2 = int(request.POST.get('num2', 0))

        if num1 > num2:
            comparison = 'num1 is greater'
        elif num1 < num2:
            comparison = 'num2 is greater'
        else:
            comparison = 'numbers are equal'

        result = {
            'number1': num1,
            'number2': num2,
            'comparison_result': comparison
        }

    return render(request, 'catalog/compare_numbers_form.html', {
        'result': result,
        'num1': num1,
        'num2': num2
    })


def low_stock_procedure(request):
    """Task 4: Simulates stored procedure to find items with stock below threshold"""
    result = None
    threshold = None

    if request.method == 'POST':
        threshold = int(request.POST.get('threshold', 0))

        result = Item.objects.filter(
            stock__quantity__lt=threshold
        ).select_related('stock').annotate(
            item_id=F('id'),
            item_description=F('description'),
            stock_quantity=F('stock__quantity')
        ).values('item_id', 'item_description', 'stock_quantity')

    return render(request, 'catalog/low_stock_form.html', {
        'result': result,
        'threshold': threshold
    })


def add_item_with_trigger(request):
    """Task 5: Add new item and simulate AFTER INSERT trigger"""
    from decimal import Decimal
    from .models import ItemHistory

    if request.method == 'POST':
        description = request.POST.get('description', '')
        cost_price = request.POST.get('cost_price', '')
        sell_price = request.POST.get('sell_price', '')

        cost_price = Decimal(cost_price) if cost_price else None
        sell_price = Decimal(sell_price) if sell_price else None

        new_item = Item.objects.create(
            description=description,
            cost_price=cost_price,
            sell_price=sell_price
        )

        # Simulate AFTER INSERT trigger
        if cost_price is None or sell_price is None:
            status = 'Price contains NULL'
        else:
            status = 'OK'

        ItemHistory.objects.create(
            item=new_item,
            item_description=new_item.description,
            status=status
        )

        return redirect('catalog:item_history')

    return render(request, 'catalog/add_item_trigger_form.html')


def item_history_view(request):
    """Task 5: Display item history table"""
    from .models import ItemHistory

    history = ItemHistory.objects.select_related('item').all().order_by('-created_at')
    return render(request, 'catalog/item_history.html', {'history': history})


def print_text_loop_procedure(request):
    """Task 6: Simulates stored procedure using LOOP to print text 3 times"""
    result = None
    text_param = None

    if request.method == 'POST':
        text_param = request.POST.get('text_param', '')

        counter = 0
        repeated_text = ''

        while True:
            counter += 1
            repeated_text += text_param + ' '

            if counter >= 3:
                break

        result = repeated_text.strip()

    return render(request, 'catalog/print_text_loop_form.html', {
        'result': result,
        'text_param': text_param
    })


def compare_tables_cursor(request):
    """Task 7: Simulates stored procedure with cursor to compare two tables"""
    from .models import ComparisonTable1, ComparisonTable2, ComparisonResult

    result = None

    if request.method == 'POST':
        if not ComparisonTable1.objects.exists():
            ComparisonTable1.objects.bulk_create([
                ComparisonTable1(id=1, value=10),
                ComparisonTable1(id=2, value=20),
                ComparisonTable1(id=3, value=30),
                ComparisonTable1(id=4, value=15),
                ComparisonTable1(id=5, value=25),
            ])
            ComparisonTable2.objects.bulk_create([
                ComparisonTable2(id=1, value=15),
                ComparisonTable2(id=2, value=20),
                ComparisonTable2(id=3, value=25),
                ComparisonTable2(id=4, value=20),
                ComparisonTable2(id=5, value=30),
            ])

        ComparisonResult.objects.all().delete()

        for t1 in ComparisonTable1.objects.all():
            try:
                t2 = ComparisonTable2.objects.get(id=t1.id)

                if t1.value > t2.value:
                    comparison_text = 't1 > t2'
                else:
                    comparison_text = 't1 ≤ t2'

                ComparisonResult.objects.create(
                    id=t1.id,
                    comparison=comparison_text
                )
            except ComparisonTable2.DoesNotExist:
                continue

        result = ComparisonResult.objects.all().order_by('id')

    return render(request, 'catalog/compare_tables.html', {
        'result': result,
        'table1': ComparisonTable1.objects.all().order_by('id'),
        'table2': ComparisonTable2.objects.all().order_by('id'),
    })
