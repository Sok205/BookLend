from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='index'),
    path('loans/', views.loans_list, name='loans_list'),
    path('search/', views.borrower_search, name='borrower_search'),
    path('counts/', views.books_borrow_count, name='books_borrow_count'),
    path('add/borrower/', views.add_borrower, name='add_borrower'),
    path('add/loan/', views.add_loan, name='add_loan'),
    path('add/book/', views.add_book, name='add_book'),
]
