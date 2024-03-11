from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from .forms import QuoteForm
from .models import Author

# Create your views here.

from .utils import get_mongodb

def main(request, page=1):
    db = get_mongodb()
    quotes = db.quotes.find()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page})


def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            # Призначення користувача цитаті
            quote.user = request.user
            # Збереження цитати в базі даних
            quote.save()
            return redirect('quotes:root')  # Перенаправлення на головну сторінку після додавання цитати
    else:
        form = QuoteForm()
    return render(request, 'quotes/add_quote.html', {'form': form})

def author_detail(request, author_slug):
    # Отримайте об'єкт автора за допомогою слага
    author = get_object_or_404(Author, slug=author_slug)
    
    # Передайте об'єкт автора в шаблон для відображення
    return render(request, 'quotes/author_detail.html', {'author': author})
