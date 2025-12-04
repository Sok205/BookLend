from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title} by {self.author}"


class Borrower(models.Model):
    family_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    contact_phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.family_name}, {self.first_name}"


class Loan(models.Model):
    book = models.ForeignKey(Book, related_name='loans', on_delete=models.CASCADE)
    borrower = models.ForeignKey(Borrower, related_name='loans', on_delete=models.CASCADE)
    loan_date = models.DateField()

    def __str__(self):
        return f"Loan #{self.pk}: {self.book} -> {self.borrower} on {self.loan_date}"

