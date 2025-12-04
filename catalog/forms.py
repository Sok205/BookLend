from django import forms
from .models import Borrower, Loan, Book


class BorrowerForm(forms.ModelForm):
    class Meta:
        model = Borrower
        fields = ['family_name', 'first_name', 'contact_phone_number']


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['book', 'borrower', 'loan_date']
        widgets = {
            'loan_date': forms.DateInput(attrs={'type': 'date'})
        }


class BorrowerSearchForm(forms.Form):
    family_name = forms.CharField(label='Borrower family name', max_length=100, required=True)


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']
