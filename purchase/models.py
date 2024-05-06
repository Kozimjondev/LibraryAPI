from django.db import models

from base.models import BaseModel
from library.models import Book
from user.models import User


# Create your models here.
class Purchase(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='purchases')
    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name='purchases')
    purchase_date = models.DateField(auto_now_add=True)
    payment_method = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.user} - {self.book}'


