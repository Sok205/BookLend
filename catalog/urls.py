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
]
