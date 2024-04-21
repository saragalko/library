from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    pseudonym = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return (f"{self.first_name} "
                f"{self.last_name if self.last_name else ''} "
                f"{self.pseudonym if self.pseudonym else ''}")

    def get_absolute_url(self):
        return reverse('author-detail', args=[self.pk])


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre)

    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre.all()])

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[self.pk])


class BookInstance(models.Model):
    STATUSES = (
        ('Available', 'Available'),
        ('On Loan', 'On Loan'),
        ('Lost', 'Lost'),
        ('On Service', 'On Service')
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUSES, max_length=50, default='Available')
    due_back = models.DateField(null=True, blank=True)
    isbn = models.CharField(max_length=13)

    def __str__(self):
        return f"{self.book.title} {self.isbn}"

    def get_absolute_url(self):
        return reverse('book-instance-detail', args=[self.pk])
