from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='index'),
    # BookLoan Tables
    path('books/', views.all_books, name='all_books'),
    path('borrowers/', views.all_borrowers, name='all_borrowers'),
    path('loans/', views.loans_list, name='loans_list'),
    # MailOrder_Sale Tables
    path('customers/', views.all_customers, name='all_customers'),
    path('items/', views.all_items, name='all_items'),
    path('orders/', views.all_orders, name='all_orders'),
    path('stock/', views.all_stock, name='all_stock'),
    path('orderlines/', views.all_orderlines, name='all_orderlines'),
    path('barcodes/', views.all_barcodes, name='all_barcodes'),
    # Queries
    path('search/', views.borrower_search, name='borrower_search'),
    path('counts/', views.books_borrow_count, name='books_borrow_count'),
    # Add Forms
    path('add/borrower/', views.add_borrower, name='add_borrower'),
    path('add/loan/', views.add_loan, name='add_loan'),
    path('add/book/', views.add_book, name='add_book'),
    # MO_Sale Queries
    path('query1/', views.query1_customers_town_h, name='query1'),
    path('query2/', views.query2_items_null, name='query2'),
    path('query3/', views.query3_customers_separate, name='query3'),
    path('query4/', views.query4_customers_concat, name='query4'),
    path('query5/', views.query5_order_details, name='query5'),
    path('query6/', views.query6_order_totals, name='query6'),
    path('query7/', views.query7_ann_stones_orders, name='query7'),
    # MySQL Stored Procedures
    path('procedure/display/', views.call_display_text, name='call_display_text'),
    path('procedure/display-three/', views.call_display_text_three_times, name='call_display_text_three_times'),
    # MoAdvanced Features
    path('advanced/order-details/', views.order_details_view, name='order_details_view'),
    path('advanced/customer-orders/', views.customer_orders_procedure, name='customer_orders_proc'),
    path('advanced/compare-numbers/', views.compare_numbers_procedure, name='compare_numbers_proc'),
    path('advanced/low-stock/', views.low_stock_procedure, name='low_stock_proc'),
    path('advanced/add-item/', views.add_item_with_trigger, name='add_item_trigger'),
    path('advanced/item-history/', views.item_history_view, name='item_history'),
    path('advanced/print-text-loop/', views.print_text_loop_procedure, name='print_text_loop'),
    path('advanced/compare-tables/', views.compare_tables_cursor, name='compare_tables_cursor'),
]
