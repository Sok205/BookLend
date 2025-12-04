from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Count

from .models import Book, Loan
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
