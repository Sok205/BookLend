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


class Customer(models.Model):
    title = models.CharField(max_length=4, blank=True, null=True)
    fname = models.CharField(max_length=32, blank=True, null=True)
    lname = models.CharField(max_length=32)
    addressline = models.CharField(max_length=64, blank=True, null=True)
    town = models.CharField(max_length=32, blank=True, null=True)
    zipcode = models.CharField(max_length=10)
    phone = models.CharField(max_length=16, blank=True, null=True)

    def __str__(self):
        return f"{self.lname}, {self.fname or ''}".strip()


class Item(models.Model):
    description = models.CharField(max_length=64)
    cost_price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    sell_price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.description


class OrderInfo(models.Model):
    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.RESTRICT)
    date_placed = models.DateField()
    date_shipped = models.DateField(blank=True, null=True)
    shipping = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"Order #{self.pk} for {self.customer} on {self.date_placed}"


class Stock(models.Model):
    # In SQL stock.item_id is the PK; model it as OneToOneField to Item with primary_key=True
    item = models.OneToOneField(Item, primary_key=True, on_delete=models.RESTRICT, related_name='stock')
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.item}: {self.quantity} in stock"


class OrderLine(models.Model):
    orderinfo = models.ForeignKey(OrderInfo, related_name='lines', on_delete=models.RESTRICT)
    item = models.ForeignKey(Item, related_name='orderlines', on_delete=models.RESTRICT)
    quantity = models.IntegerField()

    class Meta:
        unique_together = (('orderinfo', 'item'),)

    def __str__(self):
        return f"Order {self.orderinfo_id} - {self.item} x{self.quantity}"


class Barcode(models.Model):
    barcode_ean = models.CharField(max_length=13, primary_key=True)
    item = models.ForeignKey(Item, related_name='barcodes', on_delete=models.RESTRICT)

    def __str__(self):
        return self.barcode_ean


# MoAdvanced Models

class ItemHistory(models.Model):
    """Tracks item insertions - simulates AFTER INSERT trigger"""
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='history')
    item_description = models.CharField(max_length=64)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item_description} - {self.status}"


class ComparisonTable1(models.Model):
    """First table for cursor comparison demonstration"""
    id = models.IntegerField(primary_key=True)
    value = models.IntegerField()

    def __str__(self):
        return f"Table1 #{self.id}: {self.value}"


class ComparisonTable2(models.Model):
    """Second table for cursor comparison demonstration"""
    id = models.IntegerField(primary_key=True)
    value = models.IntegerField()

    def __str__(self):
        return f"Table2 #{self.id}: {self.value}"


class ComparisonResult(models.Model):
    """Result table for cursor comparison"""
    id = models.IntegerField(primary_key=True)
    comparison = models.CharField(max_length=20)

    def __str__(self):
        return f"#{self.id}: {self.comparison}"
