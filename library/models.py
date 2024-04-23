from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models import BaseModel


class Author(BaseModel):
    name = models.CharField(_("Name"), max_length=100)

    def __str__(self):
        return self.name


class Book(BaseModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.SET_NULL,
                              related_name="books",
                              null=True)
    title = models.CharField(_("Title"), max_length=100)
    author = models.ForeignKey(Author,
                               verbose_name=_("Author"),
                               related_name="books",
                               on_delete=models.CASCADE)
    publisher = models.CharField(_("Publisher"), max_length=100)
    year = models.DateField(_("Year"))
    pages = models.PositiveSmallIntegerField(_("Pages"), default=0)
    description = models.TextField(_("Description"))
    book_type = models.ManyToManyField("BookType",
                                       verbose_name=_("Book type"),
                                       related_name="books")
    image = models.ImageField(_("Image"),
                              upload_to="images/",
                              blank=True, null=True)
    file = models.FileField(_("File"),
                            upload_to="files/",
                            blank=True, null=True)
    price = models.DecimalField(_("Price"),
                                max_digits=12,
                                decimal_places=2)

    def __str__(self):
        return self.title


class BookType(BaseModel):
    name = models.CharField(_("Book Type"), max_length=100)
    description = models.TextField(_("Description"))

    def __str__(self):
        return self.name
