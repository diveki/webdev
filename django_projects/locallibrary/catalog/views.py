from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic

# Create your views here.
def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    #Available Books
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    biography_num = Book.objects.filter(genre__name__icontains='horror').count()

    context = {
        'filtered': biography_num,
        'title': 'Changed from index view',
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    paginate_by = 5
    # context_object_name = 'book_list'
    # queryset = Book.objects.filter(title__icontains='zsolt')[:5]
   # 


class BookDetailView(generic.DetailView):
    model = Book
    context_object_name = 'details'
    # template_name = 'catalog/book_detail.html'


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 5


class AuthorDetailView(generic.DetailView):
    model = Author
    # context_object_name = 'details'
    # template_name = 'catalog/author_detail.html'
