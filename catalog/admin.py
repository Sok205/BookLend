from django.contrib import admin
from .models import Book, Borrower, Loan


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')


@admin.register(Borrower)
class BorrowerAdmin(admin.ModelAdmin):
    list_display = ('family_name', 'first_name', 'contact_phone_number')


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'borrower', 'loan_date')
    list_select_related = ('book', 'borrower')

