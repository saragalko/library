from django.shortcuts import render, get_object_or_404, redirect
from catalog.models import Book, Author, Genre, BookInstance
from django.views.generic import ListView, DetailView
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required


def index(request):
    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()
    num_book_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='Available').count()

    return render(request, 'index.html', {
        "num_books": num_books,
        "num_authors": num_authors,
        "num_book_instances": num_book_instances,
        "num_instances_available": num_instances_available
    })


class AuthorListView(ListView):
    model = Author
    template_name = 'authors_list.html'
    context_object_name = 'authors_list'


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'author_detail.html'


class BookListView(ListView):
    model = Book
    template_name = 'books_list.html'
    context_object_name = 'books_list'


class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'


class BookInstanceDetailView(DetailView):
    model = BookInstance
    template_name = 'book_instance_detail.html'


@login_required
def owned_books(request):
    user = request.user
    book_instance = BookInstance.objects.filter(borrower=user)
    context = {
        'book_instance': book_instance
    }

    return render(request, 'reserved_detail.html', context)


@login_required
def reserve_book(request, book_instance_id):
    has_overdue_books = BookInstance.objects.filter(borrower=request.user, status='On Loan',
                                                    due_back__lt=timezone.now().date()).exists()
    if has_overdue_books:
        return render(request, 'reserved_detail.html',
                      {'message': 'You have expired books. It is not possible to book a new book.'})
    book_instance = get_object_or_404(BookInstance, id=book_instance_id)
    book_instance.status = 'On Loan'
    book_instance.due_back = timezone.now().date() + timedelta(weeks=2)
    book_instance.borrower = request.user
    book_instance.save()
    return render(request, 'reserved_book.html', {'book_instance': book_instance})
